from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.fit import Fit
from service.settings import ContextMenuSettings


class MutaplasmidCM(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.eventIDs = {}

    def display(self, srcContext, selection):

        # if not self.settings.get('ammoPattern'):
        #     return False

        if srcContext not in ("fittingModule") or self.mainFrame.getActiveFit() is None:
            return False

        mod = selection[0]
        if len(mod.item.mutaplasmids) == 0:
            return False

        return True

    def getText(self, itmContext, selection):
        # todo: switch between apply and remove
        return "Apply Mutaplasmid"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.skillIds = {}
        sub = wx.Menu()

        mod = selection[0]

        for item in mod.item.mutaplasmids:
            label = item.item.name
            id = ContextMenu.nextID()
            self.eventIDs[id] = item
            skillItem = wx.MenuItem(sub, id, label)
            rootMenu.Bind(wx.EVT_MENU, self.activate, skillItem)
            sub.Append(skillItem)

        return sub

    def activate(self, event):
        mutaplasmid = self.eventIDs[event.ID]
        fit = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()

        # todo: dev out function to switch module to an abyssal module. Also, maybe open item stats here automatically
        # with the attribute tab set?

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fit))

    def getBitmap(self, context, selection):
        return None


MutaplasmidCM.register()
