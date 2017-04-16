from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from gui.bitmapLoader import BitmapLoader
from service.fit import Fit
from service.settings import ContextMenuSettings


class FactorReload(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('factorReload'):
            return False

        return srcContext == "firepowerViewFull" and self.mainFrame.getActiveFit() is not None

    def getText(self, itmContext, selection):
        return "Factor in Reload Time"

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        sFit.serviceFittingOptions["useGlobalForceReload"] = not sFit.serviceFittingOptions["useGlobalForceReload"]
        fitID = self.mainFrame.getActiveFit()
        sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def getBitmap(self, context, selection):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        if fit.factorReload:
            return BitmapLoader.getBitmap("state_active_small", "gui")
        else:
            return None


FactorReload.register()
