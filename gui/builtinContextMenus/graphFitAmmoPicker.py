# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.auxFrame import AuxiliaryFrame
from gui.contextMenu import ContextMenuSingle
from service.ammo import Ammo
from service.market import Market


class GraphFitAmmoPicker(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != 'graphFitList':
            return False
        if mainItem is None or not mainItem.isFit:
            return False
        if callingWindow.graphFrame.getView().internalName != 'dmgStatsGraph':
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return 'Plot with Different Ammo...'

    def activate(self, callingWindow, fullContext, mainItem, i):
        window = AmmoPickerFrame(callingWindow, mainItem.item)
        window.Show()


GraphFitAmmoPicker.register()


class AmmoPickerFrame(AuxiliaryFrame):

    def __init__(self, parent, fit):
        super().__init__(parent, title='Choose Different Ammo', style=wx.DEFAULT_DIALOG_STYLE, resizeable=True)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        padding = 5

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        contents = AmmoPickerContents(self, fit)
        mainSizer.Add(contents, 1, wx.EXPAND | wx.ALL, padding)

        self.SetSizer(mainSizer)
        self.Layout()

        contW, contH = contents.GetVirtualSize()
        bestW = min(1000, contW + padding * 2)
        bestH = min(700, contH + padding * 2)
        self.SetSize(bestW, bestH)
        self.SetMinSize(wx.Size(int(bestW * 0.7), int(bestH * 0.7)))
        self.CenterOnParent()
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()


class AmmoPickerContents(wx.ScrolledCanvas):

    def __init__(self, parent, fit):
        wx.ScrolledCanvas.__init__(self, parent)
        self.SetScrollRate(0, 15)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        indent = 15
        mods = self.getMods(fit)
        drones = self.getDrones(fit)
        fighters = self.getFighters(fit)
        self.rbLabelMap = {}
        self.rbCheckboxMap = {}

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        firstRadio = True
        currentRb = None

        def addRadioButton(text):
            nonlocal firstRadio, currentRb
            if not firstRadio:
                rb = wx.RadioButton(self, wx.ID_ANY, text, style=wx.RB_GROUP)
                rb.SetValue(True)
                firstRadio = True
            else:
                rb = wx.RadioButton(self, wx.ID_ANY, text)
                rb.SetValue(False)
            rb.Bind(wx.EVT_RADIOBUTTON, self.rbSelected)
            currentRb = rb
            mainSizer.Add(rb, 0, wx.EXPAND | wx.ALL, 0)

        def addCheckbox(text, indentLvl=0):
            cb = wx.CheckBox(self, -1, text)
            mainSizer.Add(cb, 0, wx.EXPAND | wx.LEFT, indent * indentLvl)
            if currentRb is not None:
                self.rbCheckboxMap.setdefault(currentRb, []).append(cb)

        def addLabel(text, indentLvl=0):
            text = text[0].capitalize() + text[1:]
            label = wx.StaticText(self, wx.ID_ANY, text)
            mainSizer.Add(label, 0, wx.EXPAND | wx.LEFT, indent * indentLvl)
            if currentRb is not None:
                self.rbLabelMap.setdefault(currentRb, []).append(label)

        for modInfo, modAmmo in mods:
            text = '\n'.join('{}x {}'.format(amount, item.name) for item, amount in modInfo)
            addRadioButton(text)
            # Get actual module, as ammo getters need it
            mod = next((m for m in fit.modules if m.itemID == next(iter(modInfo))[0].ID), None)
            _, ammoTree = Ammo.getInstance().getModuleStructuredAmmo(mod)
            if len(ammoTree) == 1:
                for ammoCatName, ammos in ammoTree.items():
                    for ammo in ammos:
                        addCheckbox(ammo.name, indentLvl=1)
            else:
                for ammoCatName, ammos in ammoTree.items():
                    if len(ammos) == 1:
                        ammo = next(iter(ammos))
                        addCheckbox(ammo.name, indentLvl=1)
                    else:
                        addLabel('{}:'.format(ammoCatName), indentLvl=1)
                        for ammo in ammos:
                            addCheckbox(ammo.name, indentLvl=2)
        if drones:
            addRadioButton('Drones')
            from gui.builtinAdditionPanes.droneView import DroneView
            for drone in sorted(drones, key=DroneView.droneKey):
                addCheckbox('{}x {}'.format(drone.amount, drone.item.name), indentLvl=1)
        if fighters:
            addRadioButton('Fighters')
            from gui.builtinAdditionPanes.fighterView import FighterDisplay
            for fighter in sorted(fighters, key=FighterDisplay.fighterKey):
                addCheckbox('{}x {}'.format(fighter.amount, fighter.item.name), indentLvl=1)

        self.SetSizer(mainSizer)
        self.refreshStatus()

    def getMods(self, fit):
        sMkt = Market.getInstance()
        sAmmo = Ammo.getInstance()
        loadableChargesCache = {}
        # Modules, format: {frozenset(ammo): {item: count}}
        modsPrelim = {}
        if fit is not None:
            for mod in fit.modules:
                if not mod.canDealDamage():
                    continue
                typeID = mod.item.ID
                if typeID not in loadableChargesCache:
                    loadableChargesCache[typeID] = sAmmo.getModuleFlatAmmo(mod)
                charges = loadableChargesCache[typeID]
                # We're not interested in modules which contain no charges
                if charges:
                    data = modsPrelim.setdefault(frozenset(charges), {})
                    if mod.item not in data:
                        data[mod.item] = 0
                    data[mod.item] += 1
        # Format: [([(item, count), ...], frozenset(ammo)), ...]
        modsFinal = []
        for charges, itemCounts in modsPrelim.items():
            modsFinal.append((
                # Sort items within group
                sorted(itemCounts.items(), key=lambda i: sMkt.itemSort(i[0], reverseMktGrp=True), reverse=True),
                charges))
        # Sort item groups
        modsFinal.sort(key=lambda i: sMkt.itemSort(i[0][0][0], reverseMktGrp=True), reverse=True)
        return modsFinal

    def getDrones(self, fit):
        drones = []
        if fit is not None:
            for drone in fit.drones:
                if drone.item is None:
                    continue
                # Drones are our "ammo", so we want to pick even those which are inactive
                if drone.canDealDamage(ignoreState=True):
                    drones.append(drone)
                    continue
                if {'remoteWebifierEntity', 'remoteTargetPaintEntity'}.intersection(drone.item.effects):
                    drones.append(drone)
                    continue
        return drones

    def getFighters(self, fit):
        fighters = []
        if fit is not None:
            for fighter in fit.fighters:
                if fighter.item is None:
                    continue
                # Fighters are our "ammo" as well
                if fighter.canDealDamage(ignoreState=True):
                    fighters.append(fighter)
                    continue
                for ability in fighter.abilities:
                    if not ability.active:
                        continue
                    if ability.effect.name == 'fighterAbilityStasisWebifier':
                        fighters.append(fighter)
                        break
        return fighters

    def refreshStatus(self):
        for map in (self.rbLabelMap, self.rbCheckboxMap):
            for rb, items in map.items():
                for item in items:
                    item.Enable(rb.GetValue())

    def rbSelected(self, event):
        event.Skip()
        self.refreshStatus()
