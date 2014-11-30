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
        self.modeItems = self.ship.getModeItems()

        return srcContext == "fittingShip" and self.modeItems is not None

    def getText(self, itmContext, selection):
        return "Tactical Modes"

    def addMode(self, rootMenu, item):
        label = item.name.rsplit()[-2]
        id = wx.NewId()
        self.itemIds[id] = item
        menuItem = wx.MenuItem(rootMenu, id, label, kind=wx.ITEM_RADIO)
        rootMenu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        self.context = context
        self.itemIds = {}

        m = wx.Menu()

        for item in self.modeItems:
            menuItem = self.addMode(rootMenu, item)
            m.AppendItem(menuItem)

        return m

    def handleMode(self, event):
        item = self.itemIds[event.Id]
        print item
        # @todo fit service change mode

TacticalMode.register()
