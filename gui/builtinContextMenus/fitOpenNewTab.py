# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.builtinShipBrowser.events import FitSelected
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings


class OpenFitInNewTab(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('openFit'):
            return False
        if srcContext not in ("projectedFit", "commandFit"):
            return False
        currentFitID = self.mainFrame.getActiveFit()
        selectedFitID = selection[0].ID
        if currentFitID == selectedFitID:
            return False
        return True

    def getText(self, itmContext, selection):
        return "Open Fit in New Tab"

    def activate(self, fullContext, selection, i):
        fit = selection[0]
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fit.ID, startup=2))


OpenFitInNewTab.register()
