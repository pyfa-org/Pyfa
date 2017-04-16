from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from service.market import Market
from service.fit import Fit
from service.settings import ContextMenuSettings


class WhProjector(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('whProjector'):
            return False

        return srcContext == "projected"

    def getText(self, itmContext, selection):
        return "Add System Effects"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        sMkt = Market.getInstance()
        effdata = sMkt.getSystemWideEffects()

        self.idmap = {}
        sub = wx.Menu()

        for swType in sorted(effdata):
            subItem = wx.MenuItem(sub, wx.ID_ANY, swType)
            grandSub = wx.Menu()
            subItem.SetSubMenu(grandSub)
            sub.AppendItem(subItem)

            for swData in sorted(effdata[swType], key=lambda tpl: tpl[2]):
                wxid = ContextMenu.nextID()
                swObj, swName, swClass = swData
                self.idmap[wxid] = (swObj, swName)
                grandSubItem = wx.MenuItem(grandSub, wxid, swClass)
                if msw:
                    rootMenu.Bind(wx.EVT_MENU, self.handleSelection, grandSubItem)
                else:
                    grandSub.Bind(wx.EVT_MENU, self.handleSelection, grandSubItem)
                grandSub.AppendItem(grandSubItem)
        return sub

    def handleSelection(self, event):
        # Skip events ids that aren't mapped

        swObj, swName = self.idmap.get(event.Id, (False, False))
        if not swObj and not swName:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.project(fitID, swObj)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


WhProjector.register()
