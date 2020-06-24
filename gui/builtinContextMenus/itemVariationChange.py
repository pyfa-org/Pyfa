# noinspection PyPackageRequirements

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarFighters, getSimilarModPositions
from service.fit import Fit
from service.market import Market

_t = wx.GetTranslation


class ChangeItemToVariation(ContextMenuCombined):
    visibilitySetting = 'metaSwap'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in (
                'fittingModule',
                'droneItem',
                'fighterItem',
                'boosterItem',
                'implantItem',
                'cargoItem',
                'projectedModule',
                'projectedDrone',
                'projectedFighter'
        ):
            return False

        if mainItem is None or getattr(mainItem, 'isEmpty', False):
            return False

        self.mainVariations = Market.getInstance().getVariationsByItems((mainItem.item,))
        # No variations from current module
        if len(self.mainVariations) < 2:
            return False

        self.mainItem = mainItem
        self.selection = selection
        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext, mainItem, selection):
        return _t('Variations')

    def getSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
        self.moduleLookup = {}
        sFit = Fit.getInstance()
        sMkt = Market.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())

        def get_metalevel(x):
            return x.metaLevel or 0

        def get_metagroup(x):
            remap = {
                # We want deadspace before officer mods
                5: 6, 6: 5,
                # For structures we want t1-t2-faction
                54: 52, 52: 54
            }
            metaGroup = sMkt.getMetaGroupByItem(x)
            return remap.get(metaGroup.ID, metaGroup.ID) if metaGroup is not None else 0

        def get_boosterrank(x):
            # If we're returning a lot of items, sort my name
            if len(self.mainVariations) > 7:
                return x.name
            # Sort by booster chance to get some sort of pseudorank.
            elif 'boosterEffectChance1' in x.attributes:
                return x.attributes['boosterEffectChance1'].value
            # the "first" rank (Synth) doesn't have boosterEffectChance1. If we're not pulling back all boosters, return 0 for proper sorting
            else:
                return 0

        m = wx.Menu()

        # If on Windows we need to bind out events into the root menu, on other
        # platforms they need to go to our sub menu
        if 'wxMSW' in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m

        # Do not show abyssal items
        items = list(
                i for i in self.mainVariations
                if sMkt.getMetaGroupByItem(i) is None or sMkt.getMetaGroupByItem(i).ID != 15)
        # Sort items by metalevel, and group within that metalevel
        # Sort all items by name first
        items.sort(key=lambda x: x.name)
        # Do not do any extra sorting for implants
        if 'implantItem' in context:
            pass
        # Boosters don't have meta or anything concrete that we can rank by. Go by chance to inflict side effect
        elif 'boosterItem' in context:
            items.sort(key=get_boosterrank)
        else:
            # sort by group and meta level
            items.sort(key=get_metalevel)
            items.sort(key=get_metagroup)

        group = None
        for item in items:
            # Apparently no metaGroup for the Tech I variant:
            metaGroup = sMkt.getMetaGroupByItem(item)
            if 'subSystem' in item.effects:
                thisgroup = item.marketGroup.marketGroupName
            elif metaGroup is None:
                thisgroup = 'Tech I'
            else:
                thisgroup = metaGroup.name

            if thisgroup != group and context not in ('implantItem', 'boosterItem'):
                group = thisgroup
                id = ContextMenuCombined.nextID()
                m.Append(id, '─ %s ─' % group)
                m.Enable(id, False)

            id = ContextMenuCombined.nextID()
            mitem = wx.MenuItem(rootMenu, id, item.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleSwitch, mitem)

            self.moduleLookup[id] = item, context
            m.Append(mitem)
            mitem.Enable(self.srcContext in ('projectedModule', 'projectedDrone', 'projectedFighter') or fit.canFit(item))

        return m

    def handleSwitch(self, event):
        item, context = self.moduleLookup.get(event.Id, None)
        if item is None:
            event.Skip()
            return
        handlerMap = {
            'fittingModule': self.__handleModule,
            'droneItem': self.__handleDrone,
            'fighterItem': self.__handleFighter,
            'cargoItem': self.__handleCargo,
            'implantItem': self.__handleImplant,
            'boosterItem': self.__handleBooster,
            'projectedModule': self.__handleProjectedModule,
            'projectedDrone': self.__handleProjectedDrone,
            'projectedFighter': self.__handleProjectedFighter
        }
        handler = handlerMap.get(context)
        if handler is None:
            return
        handler(item)

    def __handleModule(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
            positions = getSimilarModPositions(fit.modules, self.mainItem)
        else:
            sMkt = Market.getInstance()
            positions = []
            for mod in self.selection:
                if mod.isEmpty:
                    continue
                if mod is self.mainItem:
                    positions.append(fit.modules.index(mod))
                    continue
                if mod not in fit.modules:
                    continue
                modVariations = sMkt.getVariationsByItems((mod.item,))
                if modVariations == self.mainVariations:
                    positions.append(fit.modules.index(mod))
        self.mainFrame.command.Submit(cmd.GuiChangeLocalModuleMetasCommand(
                fitID=fitID, positions=positions, newItemID=varItem.ID))

    def __handleDrone(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        sMkt = Market.getInstance()
        positions = []
        for drone in self.selection:
            if drone not in fit.drones:
                continue
            if drone is self.mainItem:
                positions.append(fit.drones.index(drone))
                continue
            droneVariations = sMkt.getVariationsByItems((drone.item,))
            if droneVariations == self.mainVariations:
                positions.append(fit.drones.index(drone))
        self.mainFrame.command.Submit(cmd.GuiChangeLocalDroneMetasCommand(
                fitID=fitID, positions=positions, newItemID=varItem.ID))

    def __handleFighter(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
            fighters = getSimilarFighters(fit.fighters, self.mainItem)
        else:
            fighters = self.selection
        sMkt = Market.getInstance()
        positions = []
        for fighter in fighters:
            if fighter not in fit.fighters:
                continue
            if fighter is self.mainItem:
                positions.append(fit.fighters.index(fighter))
                continue
            fighterVariations = sMkt.getVariationsByItems((fighter.item,))
            if fighterVariations == self.mainVariations:
                positions.append(fit.fighters.index(fighter))
        self.mainFrame.command.Submit(cmd.GuiChangeLocalFighterMetasCommand(
                fitID=fitID, positions=positions, newItemID=varItem.ID))

    def __handleCargo(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        sMkt = Market.getInstance()
        itemIDs = []
        for cargo in self.selection:
            if cargo is self.mainItem:
                itemIDs.append(cargo.itemID)
                continue
            cargoVariations = sMkt.getVariationsByItems((cargo.item,))
            if cargoVariations == self.mainVariations:
                itemIDs.append(cargo.itemID)
        self.mainFrame.command.Submit(cmd.GuiChangeCargoMetasCommand(
                fitID=fitID, itemIDs=itemIDs, newItemID=varItem.ID))

    def __handleImplant(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        implant = self.mainItem
        if implant in fit.implants:
            position = fit.implants.index(implant)
            self.mainFrame.command.Submit(cmd.GuiChangeImplantMetaCommand(
                    fitID=fitID, position=position, newItemID=varItem.ID))

    def __handleBooster(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        booster = self.mainItem
        if booster in fit.boosters:
            position = fit.boosters.index(booster)
            self.mainFrame.command.Submit(cmd.GuiChangeBoosterMetaCommand(
                    fitID=fitID, position=position, newItemID=varItem.ID))

    def __handleProjectedModule(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
            positions = getSimilarModPositions(fit.projectedModules, self.mainItem)
        else:
            sMkt = Market.getInstance()
            positions = []
            for mod in self.selection:
                if mod is self.mainItem:
                    positions.append(fit.projectedModules.index(mod))
                    continue
                if mod not in fit.projectedModules:
                    continue
                modVariations = sMkt.getVariationsByItems((mod.item,))
                if modVariations == self.mainVariations:
                    positions.append(fit.projectedModules.index(mod))
        self.mainFrame.command.Submit(cmd.GuiChangeProjectedModuleMetasCommand(
                fitID=fitID, positions=positions, newItemID=varItem.ID))

    def __handleProjectedDrone(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        sMkt = Market.getInstance()
        itemIDs = []
        for drone in self.selection:
            if drone not in fit.projectedDrones:
                continue
            if drone is self.mainItem:
                itemIDs.append(drone.itemID)
                continue
            droneVariations = sMkt.getVariationsByItems((drone.item,))
            if droneVariations == self.mainVariations:
                itemIDs.append(drone.itemID)
        self.mainFrame.command.Submit(cmd.GuiChangeProjectedDroneMetasCommand(
                fitID=fitID, itemIDs=itemIDs, newItemID=varItem.ID))

    def __handleProjectedFighter(self, varItem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
            fighters = getSimilarFighters(fit.projectedFighters, self.mainItem)
        else:
            fighters = self.selection
        sMkt = Market.getInstance()
        positions = []
        for fighter in fighters:
            if fighter not in fit.projectedFighters:
                continue
            if fighter is self.mainItem:
                positions.append(fit.projectedFighters.index(fighter))
                continue
            fighterVariations = sMkt.getVariationsByItems((fighter.item,))
            if fighterVariations == self.mainVariations:
                positions.append(fit.projectedFighters.index(fighter))
        self.mainFrame.command.Submit(cmd.GuiChangeProjectedFighterMetasCommand(
                fitID=fitID, positions=positions, newItemID=varItem.ID))


ChangeItemToVariation.register()
