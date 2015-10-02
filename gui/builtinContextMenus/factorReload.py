from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.globalEvents as GE
import wx
from gui.bitmapLoader import BitmapLoader

class FactorReload(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext == "firepowerViewFull" and self.mainFrame.getActiveFit() is not None

    def getText(self, itmContext, selection):
        return "Factor in Reload Time"

    def activate(self, fullContext, selection, i):
        sFit = service.Fit.getInstance()
        sFit.serviceFittingOptions["useGlobalForceReload"] = not sFit.serviceFittingOptions["useGlobalForceReload"]
        fitID = self.mainFrame.getActiveFit()
        sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def getBitmap(self, context, selection):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        if fit.factorReload:
            return BitmapLoader.getBitmap("state_active_small", "gui")
        else:
            return None


FactorReload.register()
