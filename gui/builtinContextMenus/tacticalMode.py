# noinspection PyPackageRequirements
import wx
from gui.contextMenu import ContextMenu
import gui.mainFrame

import gui.globalEvents as GE
from service.fit import Fit
from service.settings import ContextMenuSettings


class TacticalMode(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('tacticalMode'):
            return False

        if self.mainFrame.getActiveFit() is None or srcContext != "fittingShip":
            return False

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        self.modes = fit.ship.modes
        self.currMode = fit.mode

        return srcContext == "fittingShip" and self.modes is not None

    def getText(self, itmContext, selection):
        return "Tactical Mode"

    def addMode(self, menu, mode):
        label = mode.item.name.rsplit()[-2]
        id = ContextMenu.nextID()
        self.modeIds[id] = mode
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_RADIO)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.modeIds = {}

        sub = wx.Menu()

        for mode in self.modes:
            menuItem = self.addMode(rootMenu if msw else sub, mode)
            sub.Append(menuItem)
            menuItem.Check(self.currMode.item == mode.item)

        return sub

    def handleMode(self, event):
        item = self.modeIds[event.Id]
        if item is False or item not in self.modes:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.setMode(fitID, self.modeIds[event.Id])
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


TacticalMode.register()
