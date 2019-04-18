# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.market import Market
from service.settings import ContextMenuSettings


class ChangeItemToVariation(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
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

        # Check if list of variations is same for all of selection
        # If not - don't show the menu
        mkt = Market.getInstance()
        self.variations = None
        for i in selection:
            variations = mkt.getVariationsByItems([i.item])
            if self.variations is None:
                self.variations = variations
            else:
                if variations != self.variations:
                    return False

        self.selection = selection

        if len(self.variations) == 1:
            return False  # no variations from current module

        return True

    def getText(self, itmContext, selection):
        return 'Variations'

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        self.moduleLookup = {}
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())

        def get_metalevel(x):
            if 'metaLevel' not in x.attributes:
                return 0
            return x.attributes['metaLevel'].value

        def get_metagroup(x):
            return x.metaGroup.ID if x.metaGroup is not None else 0

        def get_boosterrank(x):
            # If we're returning a lot of items, sort my name
            if len(self.variations) > 7:
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
        items = list(self.variations)
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
                id = ContextMenu.nextID()
                m.Append(id, '─ %s ─' % group)
                m.Enable(id, False)

            id = ContextMenu.nextID()
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
            positions = [mod.modPosition for mod in self.selection]
            self.mainFrame.command.Submit(cmd.GuiChangeLocalModuleMetasCommand(
                fitID=fitID, positions=positions, newItemID=item.ID))
        elif context == 'droneItem':
            position = fit.drones.index(self.selection[0])
            self.mainFrame.command.Submit(cmd.GuiChangeLocalDroneMetaCommand(
                fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'fighterItem':
            position = fit.fighters.index(self.selection[0])
            self.mainFrame.command.Submit(cmd.GuiChangeLocalFighterMetaCommand(
                fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'implantItem':
            position = fit.implants.index(self.selection[0])
            self.mainFrame.command.Submit(cmd.GuiChangeImplantMetaCommand(
                fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'boosterItem':
            position = fit.boosters.index(self.selection[0])
            self.mainFrame.command.Submit(cmd.GuiChangeBoosterMetaCommand(
                fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'cargoItem':
            self.mainFrame.command.Submit(cmd.GuiChangeCargoMetaCommand(
                fitID=fitID, itemID=self.selection[0].itemID, newItemID=item.ID))
        elif context == 'projectedModule':
            position = fit.projectedModules.index(self.selection[0])
            self.mainFrame.command.Submit(cmd.GuiChangeProjectedModuleMetaCommand(
                fitID=fitID, position=position, newItemID=item.ID))
        elif context == 'projectedDrone':
            self.mainFrame.command.Submit(cmd.GuiChangeProjectedDroneMetaCommand(
                fitID=fitID, itemID=self.selection[0].itemID, newItemID=item.ID))
        elif context == 'projectedFighter':
            position = fit.projectedFighters.index(self.selection[0])
            self.mainFrame.command.Submit(cmd.GuiChangeProjectedFighterMetaCommand(
                fitID=fitID, position=position, newItemID=item.ID))


ChangeItemToVariation.register()
