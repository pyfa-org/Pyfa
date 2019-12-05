# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarModPositions
from service.ammo import Ammo
from service.fit import Fit


class ChangeModuleAmmo(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        # Format: {type ID: set(loadable, charges)}
        self.loadableChargesCache = {}

    def display(self, callingWindow, srcContext, mainItem, selection):
        if srcContext not in ('fittingModule', 'projectedModule'):
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        self.mainCharges = self._getAmmo(mainItem)
        if not self.mainCharges:
            return False

        self.module = mainItem
        self.selection = selection
        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext, mainItem, selection):
        return 'Charge'

    def _getAmmo(self, mod):
        if mod.itemID is None:
            return set()
        if mod.itemID not in self.loadableChargesCache:
            self.loadableChargesCache[mod.itemID] = Ammo.getInstance().getModuleFlatAmmo(mod)
        return self.loadableChargesCache[mod.itemID]

    def _addCharge(self, menu, charge):
        id_ = ContextMenuCombined.nextID()
        name = charge.name if charge is not None else 'Empty'
        self.chargeEventMap[id_] = charge
        item = wx.MenuItem(menu, id_, name)
        menu.Bind(wx.EVT_MENU, self.handleAmmoSwitch, item)
        item.charge = charge
        if charge is not None and charge.iconID is not None:
            bitmap = BitmapLoader.getBitmap(charge.iconID, 'icons')
            if bitmap is not None:
                item.SetBitmap(bitmap)
        return item

    @staticmethod
    def _addSeparator(m, text):
        id_ = ContextMenuCombined.nextID()
        m.Append(id_, '─ %s ─' % text)
        m.Enable(id_, False)

    def getSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        msw = True if 'wxMSW' in wx.PlatformInfo else False
        menu = wx.Menu()
        self.chargeEventMap = {}
        modType, chargeDict = Ammo.getInstance().getModuleStructuredAmmo(self.module, ammo=self.mainCharges)
        if modType == 'ddTurret':
            self._addSeparator(menu, 'Long Range')
            menuItems = []
            for charges in chargeDict.values():
                if len(charges) == 1:
                    menuItems.append(self._addCharge(rootMenu if msw else menu, charges[0]))
                else:
                    baseCharge = charges[0]
                    menuItem = self._addCharge(rootMenu if msw else menu, baseCharge)
                    menuItems.append(menuItem)
                    subMenu = wx.Menu()
                    subMenu.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
                    menuItem.SetSubMenu(subMenu)
                    self._addSeparator(subMenu, 'Less Damage')
                    for charge in charges:
                        subMenu.Append(self._addCharge(rootMenu if msw else subMenu, charge))
                    self._addSeparator(subMenu, 'More Damage')
            for menuItem in menuItems:
                menu.Append(menuItem)
            self._addSeparator(menu, 'Short Range')
        elif modType == 'ddMissile':
            menuItems = []
            for chargeCatName, charges in chargeDict.items():
                menuItem = wx.MenuItem(menu, wx.ID_ANY, chargeCatName.capitalize())
                menuItems.append(menuItem)
                subMenu = wx.Menu()
                subMenu.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
                menuItem.SetSubMenu(subMenu)
                self._addSeparator(subMenu, 'Less Damage')
                for charge in charges:
                    subMenu.Append(self._addCharge(rootMenu if msw else subMenu, charge))
                self._addSeparator(subMenu, 'More Damage')
            for menuItem in menuItems:
                menu.Append(menuItem)
        elif modType == 'general':
            for charge in chargeDict['general']:
                menu.Append(self._addCharge(rootMenu if msw else menu, charge))
        menu.Append(self._addCharge(rootMenu if msw else menu, None))
        return menu

    def handleAmmoSwitch(self, event):
        charge = self.chargeEventMap.get(event.Id, False)
        if charge is False:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        # Switch in selection or all modules, depending on modifier key state and settings
        switchAll = sFit.serviceFittingOptions['ammoChangeAll'] is not (wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL))
        if switchAll:
            if self.srcContext == 'fittingModule':
                command = cmd.GuiChangeLocalModuleChargesCommand
                modContainer = fit.modules
            elif self.srcContext == 'projectedModule':
                command = cmd.GuiChangeProjectedModuleChargesCommand
                modContainer = fit.projectedModules
            else:
                return
            positions = getSimilarModPositions(modContainer, self.module)
            self.mainFrame.command.Submit(command(
                fitID=fitID,
                positions=positions,
                chargeItemID=charge.ID if charge is not None else None))
        else:
            if self.srcContext == 'fittingModule':
                command = cmd.GuiChangeLocalModuleChargesCommand
                modContainer = fit.modules
            elif self.srcContext == 'projectedModule':
                command = cmd.GuiChangeProjectedModuleChargesCommand
                modContainer = fit.projectedModules
            else:
                return
            positions = []
            for position, mod in enumerate(modContainer):
                if mod in self.selection:
                    modCharges = self._getAmmo(mod)
                    if modCharges.issubset(self.mainCharges):
                        positions.append(position)
            self.mainFrame.command.Submit(command(
                fitID=fitID,
                positions=positions,
                chargeItemID=charge.ID if charge is not None else None))


ChangeModuleAmmo.register()
