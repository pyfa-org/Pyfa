# -*- coding: utf-8 -*-
from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service
import wx
import gui.globalEvents as GE

class MetaSwap(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):

        if self.mainFrame.getActiveFit() is None or srcContext not in (
                "fittingModule",
                "droneItem",
                "fighterItem",
                "boosterItem",
                "implantItem",
        ):
            return False

        # Check if list of variations is same for all of selection
        # If not - don't show the menu
        mkt = service.Market.getInstance()
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
            if "metaLevel" not in x.attributes: return 0
            return x.attributes["metaLevel"].value

        def get_metagroup(x):
            return x.metaGroup.ID if x.metaGroup is not None else 0

        m = wx.Menu()

        # If on Windows we need to bind out events into the root menu, on other
        # platforms they need to go to our sub menu
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m

        # Sort items by metalevel, and group within that metalevel
        items = list(self.variations)
        items.sort(key=get_metalevel)
        items.sort(key=get_metagroup)

        group = None
        for item in items:
            # Apparently no metaGroup for the Tech I variant:
            if item.metaGroup is None:
                thisgroup = "Tech I"
            else:
                thisgroup = item.metaGroup.name

            if thisgroup != group:
                group = thisgroup
                id = ContextMenu.nextID()
                m.Append(id, u'─ %s ─' % group)
                m.Enable(id, False)

            id = ContextMenu.nextID()
            mitem = wx.MenuItem(rootMenu, id, item.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleModule, mitem)
            self.moduleLookup[id] = item
            m.AppendItem(mitem)
        return m

    def handleModule(self, event):
        item = self.moduleLookup.get(event.Id, None)
        if item is None:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        
        for selected_item in self.selection:
            if type(selected_item).__name__== 'Module':
                pos = fit.modules.index(selected_item)
                sFit.changeModule(fitID, pos, item.ID)

            elif type(selected_item).__name__== 'Drone':
                drone_count = None
                drone_index = None

                for idx, drone_stack in enumerate(fit.drones):
                    if drone_stack is selected_item:
                        drone_count = drone_stack.amount
                        sFit.removeDrone(fitID, idx, drone_count)
                        break

                if drone_count:
                    sFit.addDrone(fitID, item.ID, drone_count)

            elif type(selected_item).__name__== 'Fighter':
                fighter_count = None
                fighter_index = None

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

                        sFit.removeFighter(fitID, idx)
                        break

                sFit.addFighter(fitID, item.ID)

            elif type(selected_item).__name__== 'Booster':
                for idx, booster_stack in enumerate(fit.boosters):
                    if booster_stack is selected_item:
                        sFit.removeBooster(fitID, idx)
                        sFit.addBooster(fitID, item.ID)
                        break

            elif type(selected_item).__name__== 'Implant':
                for idx, implant_stack in enumerate(fit.implants):
                    if implant_stack is selected_item:
                        sFit.removeImplant(fitID, idx)
                        sFit.addImplant(fitID, item.ID, False)
                        break

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

MetaSwap.register()
