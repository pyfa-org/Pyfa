# -*- coding: utf-8 -*-
from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service
import wx
import gui.globalEvents as GE

# TODO:
# Handle multiple selection better
# Icons?
# Submenu for officer?

class MetaSwap(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):

        if self.mainFrame.getActiveFit() is None or srcContext not in ("fittingModule", "projectedModule"):
            return False

        self.module = selection[0]

        return True

    def getText(self, itmContext, selection):
        return "Variations"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        self.moduleLookup = {}

        def get_metalevel(x):
            return x.attributes["metaLevel"].value

        m = wx.Menu()
        mkt = service.Market.getInstance()
        items = list(mkt.getVariationsByItems([selection[0].item]))
        items.sort(key=get_metalevel)
        group = None
        for item in items:
            # Apparently no metaGroup for the Tech I variant:
            if item.metaGroup is None:
                thisgroup = "Tech I"
            else:
                thisgroup = item.metaGroup.name

            if thisgroup != group:
                group = thisgroup
                id = wx.NewId()
                m.Append(id, u'─ %s ─' % group)
                m.Enable(id, False)

            id = wx.NewId()
            mitem = wx.MenuItem(rootMenu, id, item.name)
            rootMenu.Bind(wx.EVT_MENU, self.handleModule, mitem)
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
        
        pos = fit.modules.index(self.module)
        sFit.changeModule(fitID, pos, item.ID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

MetaSwap.register()
