from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
from gui.shipBrowser import FitSelected


class OpenFit(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext == "projectedFit"

    def getText(self, itmContext, selection):
        return "Open Fit in New Tab"

    def activate(self, fullContext, selection, i):
        fit = selection[0]
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fit.ID, startup=2))


OpenFit.register()
