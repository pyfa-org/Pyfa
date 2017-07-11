# noinspection PyPackageRequirements
import wx
from gui.contextMenu import ContextMenu
import gui.mainFrame
from gui.builtinShipBrowser.events import Stage3Selected
from service.fit import Fit
from service.settings import ContextMenuSettings


class ShipJump(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('shipJump'):
            return False

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
