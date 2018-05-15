# coding: utf-8

# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from service.market import Market
import gui.mainFrame
import gui.globalEvents as GE
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings
from eos.saveddata.booster import Booster
from eos.saveddata.module import Module
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.implant import Implant
from eos.saveddata.cargo import Cargo


class MetaSwap(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('metaSwap'):
            return False

        if self.mainFrame.getActiveFit() is None or srcContext not in (
                "fittingModule",
                "droneItem",
                "fighterItem",
                "boosterItem",
                "implantItem",
                "cargoItem",
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
        return "Variations"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        self.moduleLookup = {}

        def get_metalevel(x):
            if "metaLevel" not in x.attributes:
                return 0
            return x.attributes["metaLevel"].value

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
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m

        # Sort items by metalevel, and group within that metalevel
        items = list(self.variations)
        print(context)
        if "implantItem" in context:
            # sort implants based on name
            items.sort(key=lambda x: x.name)
        elif "boosterItem" in context:
            # boosters don't have meta or anything concrete that we can rank by. Go by chance to inflict side effect
            items.sort(key=get_boosterrank)
        else:
            # sort by group and meta level
            items.sort(key=get_metalevel)
            items.sort(key=get_metagroup)

        group = None
        for item in items:
            # Apparently no metaGroup for the Tech I variant:
            if "subSystem" in item.effects:
                thisgroup = item.marketGroup.marketGroupName
            elif item.metaGroup is None:
                thisgroup = "Tech I"
            else:
                thisgroup = item.metaGroup.name

            if thisgroup != group and context not in ("implantItem", "boosterItem"):
                group = thisgroup
                id = ContextMenu.nextID()
                m.Append(id, '─ %s ─' % group)
                m.Enable(id, False)

            id = ContextMenu.nextID()
            mitem = wx.MenuItem(rootMenu, id, item.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleModule, mitem)
            self.moduleLookup[id] = item
            m.Append(mitem)
        return m

    def handleModule(self, event):
        item = self.moduleLookup.get(event.Id, None)
        if item is None:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        for selected_item in self.selection:
            if isinstance(selected_item, Module):
                pos = fit.modules.index(selected_item)
                sFit.changeModule(fitID, pos, item.ID)

            elif isinstance(selected_item, Drone):
                drone_count = None

                for idx, drone_stack in enumerate(fit.drones):
                    if drone_stack is selected_item:
                        drone_count = drone_stack.amount
                        sFit.removeDrone(fitID, idx, drone_count, False)
                        break

                if drone_count:
                    sFit.addDrone(fitID, item.ID, drone_count, True)

            elif isinstance(selected_item, Fighter):
                fighter_count = None

                for idx, fighter_stack in enumerate(fit.fighters):
                    # Right now fighters always will have max stack size.
                    # Including this for future improvement, so if adjustable
                    # fighter stacks get added we're ready for it.
                    if fighter_stack is selected_item:
                        if fighter_stack.amount > 0:
                            fighter_count = fighter_stack.amount
                        elif fighter_stack.amount == -1:
                            fighter_count = fighter_stack.amountActive
                        else:
                            fighter_count.amount = 0

                        sFit.removeFighter(fitID, idx, False)
                        break

                sFit.addFighter(fitID, item.ID, True)

            elif isinstance(selected_item, Booster):
                for idx, booster_stack in enumerate(fit.boosters):
                    if booster_stack is selected_item:
                        sFit.removeBooster(fitID, idx, False)
                        sFit.addBooster(fitID, item.ID, True)
                        break

            elif isinstance(selected_item, Implant):
                for idx, implant_stack in enumerate(fit.implants):
                    if implant_stack is selected_item:
                        sFit.removeImplant(fitID, idx, False)
                        sFit.addImplant(fitID, item.ID, True)
                        break

            elif isinstance(selected_item, Cargo):
                for idx, cargo_stack in enumerate(fit.cargo):
                    if cargo_stack is selected_item:
                        sFit.removeCargo(fitID, idx)
                        sFit.addCargo(fitID, item.ID, cargo_stack.amount, True)
                        break

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


MetaSwap.register()
