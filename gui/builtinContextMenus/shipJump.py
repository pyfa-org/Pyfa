# noinspection PyPackageRequirements

import wx

import gui.mainFrame
from gui.builtinShipBrowser.events import Stage3Selected
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit

_t = wx.GetTranslation


class JumpToShip(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext != "fittingShip":
            return False
        fitTabSelected = self.mainFrame.notebookBrowsers.GetSelection() == 1
        if not fitTabSelected:
            return True
        browsingStage = self.mainFrame.shipBrowser.GetActiveStage()
        if browsingStage != 3:
            return True
        fitID = self.mainFrame.getActiveFit()
        ship = Fit.getInstance().getFit(fitID).ship
        browsingShipID = self.mainFrame.shipBrowser.GetStageData(browsingStage)
        if browsingShipID != ship.item.ID:
            return True
        return False

    def getText(self, callingWindow, itmContext):
        return _t("Open in Fitting Browser")

    def activate(self, callingWindow, fullContext, i):
        fitID = self.mainFrame.getActiveFit()
        ship = Fit.getInstance().getFit(fitID).ship
        self.mainFrame.notebookBrowsers.SetSelection(1)
        wx.PostEvent(self.mainFrame.shipBrowser, Stage3Selected(shipID=ship.item.ID, back=True))


JumpToShip.register()
