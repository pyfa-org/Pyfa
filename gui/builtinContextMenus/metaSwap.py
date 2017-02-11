# coding: utf-8

# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from service.market import Market
import gui.mainFrame
import gui.globalEvents as GE
from gui.contextMenu import ContextMenu


class MetaSwap(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):

        if self.mainFrame.getActiveFit() is None or srcContext not in ("fittingModule",):
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

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        for mod in self.selection:
            pos = fit.modules.index(mod)
            sFit.changeModule(fitID, pos, item.ID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


MetaSwap.register()
