from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import eos.types
import gui.mainFrame
import service
import gui.globalEvents as GE
import wx

class ImplantSets(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext == "implantView"

    def getText(self, itmContext, selection):
        return "Add Implant Set"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        m = wx.Menu()
        bindmenu = rootMenu if "wxMSW" in wx.PlatformInfo else m

        sIS = service.ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        self.idmap = {}

        for set in implantSets:
            id = wx.NewId()
            mitem = wx.MenuItem(rootMenu, id, set.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.idmap[id] = set
            m.AppendItem(mitem)

        return m

    def handleSelection(self, event):
        set = self.idmap.get(event.Id, None)

        if set is None:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        for implant in set.implants:
            print implant.item.ID, implant.item.name
            sFit.addImplant(fitID, implant.item.ID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


ImplantSets.register()
