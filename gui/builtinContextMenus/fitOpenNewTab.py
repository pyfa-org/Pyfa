# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.builtinShipBrowser.events import FitSelected
from gui.contextMenu import ContextMenuSingle
from service.settings import ContextMenuSettings


class OpenFitInNewTab(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem):
        if srcContext not in ("projectedFit", "commandFit"):
            return False

        if mainItem is None:
            return False

        currentFitID = self.mainFrame.getActiveFit()
        selectedFitID = mainItem.ID
        if currentFitID == selectedFitID:
            return False
        return True

    def getText(self, itmContext, mainItem):
        return "Open Fit in New Tab"

    def activate(self, fullContext, mainItem, i):
        wx.PostEvent(self.mainFrame, FitSelected(fitID=mainItem.ID, startup=2))


OpenFitInNewTab.register()
