from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
import service
import wx

class WhProjector(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext in ("projectedDrone", "projectedModule", "projectedCharge", "projectedFit", "projectedNone")

    def getText(self, itmContext, selection):
        return "Add System Effects"

    def activate(self, fullContext, selection, i):
        pass

    def getSubMenu(self, context, selection, menu, i):
        self.idmap = {}
        menu.Bind(wx.EVT_MENU, self.handleSelection)
        m = wx.Menu()
        sMkt = service.Market.getInstance()
        effdata = sMkt.getSystemWideEffects()
        for swType in sorted(effdata):
            item = wx.MenuItem(m, wx.ID_ANY, swType)
            sub = wx.Menu()
            sub.Bind(wx.EVT_MENU, self.handleSelection)
            item.SetSubMenu(sub)
            m.AppendItem(item)
            for swData in sorted(effdata[swType], key=lambda tpl: tpl[2]):
                wxid = wx.NewId()
                swObj, swName, swClass = swData
                self.idmap[wxid] = (swObj, swName)
                subitem = wx.MenuItem(sub, wxid, swClass)
                sub.AppendItem(subitem)
        return m


    def handleSelection(self, event):
        swObj, swName = self.idmap[event.Id]
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.project(fitID, swObj)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

WhProjector.register()
