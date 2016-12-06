import wx

import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui.shipBrowser import Stage3Selected
from gui_service.fit import Fit


class ShipJump(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext == "fittingShip"

    def getText(self, itmContext, selection):
        return "Open in Fitting Browser"

    def activate(self, fullContext, selection, i):
        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        stuff = sFit.getFit(fitID).ship
        groupID = stuff.item.group.ID

        self.mainFrame.notebookBrowsers.SetSelection(1)
        wx.PostEvent(self.mainFrame.shipBrowser, Stage3Selected(shipID=stuff.item.ID, back=groupID))


ShipJump.register()
