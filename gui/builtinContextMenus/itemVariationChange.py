# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarModPositions
from service.fit import Fit
from service.market import Market
from service.settings import ContextMenuSettings


class ChangeItemToVariation(ContextMenuCombined):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if not self.settings.get('metaSwap'):
            return False

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
        return True

    def getText(self, itmContext, mainItem, selection):
        return 'Variations'

    def getSubMenu(self, context, mainItem, selection, rootMenu, i, pitem):
        self.moduleLookup = {}
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())

        def get_metalevel(x):
            if 'metaLevel' not in x.attributes:
                return 0
            return x.attributes['metaLevel'].value

        def get_metagroup(x):
            # We want deadspace before officer mods
            remap = {5: 6, 6: 5}
            return remap.get(x.metaGroup.ID, x.metaGroup.ID) if x.metaGroup is not None else 0

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

        # Sort items by metalevel, and group within that metalevel
        items = list(self.mainVariations)
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
            if 'subSystem' in item.effects:
                thisgroup = item.marketGroup.marketGroupName
            elif item.metaGroup is None:
                thisgroup = 'Tech I'
            else:
                thisgroup = item.metaGroup.name

            if thisgroup != group and context not in ('implantItem', 'boosterItem'):
                group = thisgroup
                id = ContextMenuCombined.nextID()
                m.Append(id, '─ %s ─' % group)
                m.Enable(id, False)

            id = ContextMenuCombined.nextID()
            mitem = wx.MenuItem(rootMenu, id, item.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleModule, mitem)

            self.moduleLookup[id] = item, context
            m.Append(mitem)
            mitem.Enable(fit.canFit(item))

        return m

    def handleModule(self, event):
        item, context = self.moduleLookup.get(event.Id, None)
        if item is None:
            event.Skip()
            return
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if context == 'fittingModule':
            if wx.GetMouseState().altDown:
                positions = getSimilarModPositions(fit.modules, self.mainItem)
            else:
                positions = []
                for position, mod in enumerate(fit.modules):
                    if mod in self.selection:
                        if mod.isEmpty:
                            continue
                        modVariations = Market.getInstance().getVariationsByItems((mod.item,))
                        if modVariations == self.mainVariations:
                            positions.append(position)
            self.mainFrame.command.Submit(cmd.GuiChangeLocalModuleMetasCommand(
                fitID=fitID, positions=positions, newItemID=item.ID))
        elif context == 'droneItem':
            drone = self.mainItem
            if drone in fit.drones:
                position = fit.drones.index(drone)
                self.mainFrame.command.Submit(cmd.GuiChangeLocalDroneMetaCommand(
                    fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'fighterItem':
            fighter = self.mainItem
            if fighter in fit.fighters:
                position = fit.fighters.index(fighter)
                self.mainFrame.command.Submit(cmd.GuiChangeLocalFighterMetaCommand(
                    fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'implantItem':
            implant = self.mainItem
            if implant in fit.implants:
                position = fit.implants.index(implant)
                self.mainFrame.command.Submit(cmd.GuiChangeImplantMetaCommand(
                    fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'boosterItem':
            booster = self.mainItem
            if booster in fit.boosters:
                position = fit.boosters.index(booster)
                self.mainFrame.command.Submit(cmd.GuiChangeBoosterMetaCommand(
                    fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'cargoItem':
            cargo = self.mainItem
            self.mainFrame.command.Submit(cmd.GuiChangeCargoMetaCommand(
                fitID=fitID, itemID=cargo.itemID, newItemID=item.ID))
        elif context == 'projectedModule':
            mod = self.mainItem
            if mod in fit.projectedModules:
                position = fit.projectedModules.index(mod)
                self.mainFrame.command.Submit(cmd.GuiChangeProjectedModuleMetaCommand(
                    fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'projectedDrone':
            drone = self.mainItem
            self.mainFrame.command.Submit(cmd.GuiChangeProjectedDroneMetaCommand(
                fitID=fitID, itemID=drone.itemID, newItemID=item.ID))
        elif context == 'projectedFighter':
            fighter = self.mainItem
            if fighter in fit.projectedFighters:
                position = fit.projectedFighters.index(fighter)
                self.mainFrame.command.Submit(cmd.GuiChangeProjectedFighterMetaCommand(
                    fitID=fitID, position=position, newItemID=item.ID))


ChangeItemToVariation.register()
