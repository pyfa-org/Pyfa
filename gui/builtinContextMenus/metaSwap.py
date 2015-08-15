# -*- coding: utf-8 -*-
from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service
import wx

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
            name = item.name
            m.AppendItem(wx.MenuItem(rootMenu, id, name))
        return m

MetaSwap.register()
