import wx
from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
from gui.shipBrowser import Stage3Selected

class TacticalMode(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        self.ship = sFit.getFit(fitID).ship
        self.modes = self.ship.getValidModes()

        if not srcContext in ("fittingShip") or self.modes is None:
            return False

        return True

    def getText(self, itmContext, selection):
        return "Modes"

    def handleModeChange(self, event):
        mode = self.modeIds[event.Id]
        print mode
        # @todo fit service change mode

    def addMode(self, menu, mode):
        label = mode.item.name.rsplit()[-2]
        id = wx.NewId()
        self.modeIds[id] = mode
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleModeChange, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, menu, i, pitem):
        sub = wx.Menu()
        self.modeIds = {}
        # Items that have a parent
        for mode in self.modes:
            sub.AppendItem(self.addMode(sub, mode))

        return sub

TacticalMode.register()
