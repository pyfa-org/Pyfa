# noinspection PyPackageRequirements
import wx

from gui.contextMenu import ContextMenuUnconditional
from service.implantSet import ImplantSets as s_ImplantSets


class ImplantSetLoad(ContextMenuUnconditional):

    def display(self, callingWindow, srcContext):

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        if len(implantSets) == 0:
            return False
        return srcContext in ("implantItemMisc", "implantEditor")

    def getText(self, callingWindow, itmContext):
        return "Load Implant Set"

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        m = wx.Menu()
        bindmenu = rootMenu if "wxMSW" in wx.PlatformInfo else m

        sIS = s_ImplantSets.getInstance()
        implantSets = sIS.getImplantSetList()

        self.context = context
        self.callingWindow = callingWindow

        self.idmap = {}

        for set in sorted(implantSets, key=lambda i: i.name):
            id = ContextMenuUnconditional.nextID()
            mitem = wx.MenuItem(rootMenu, id, set.name)
            bindmenu.Bind(wx.EVT_MENU, self.handleSelection, mitem)
            self.idmap[id] = set
            m.Append(mitem)

        return m

    def handleSelection(self, event):
        impSet = self.idmap.get(event.Id, None)
        if impSet is None:
            event.Skip()
            return

        self.callingWindow.addImplantSet(impSet)


ImplantSetLoad.register()
