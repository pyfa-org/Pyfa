from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from service.fit import Fit
from service.settings import ContextMenuSettings


class FactorReload(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('factorReload'):
            return False

        return srcContext == "firepowerViewFull"

    @property
    def enabled(self):
        return self.mainFrame.getActiveFit() is not None

    def getText(self, itmContext, selection):
        return "Factor in Reload Time"

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        sFit.serviceFittingOptions["useGlobalForceReload"] = not sFit.serviceFittingOptions["useGlobalForceReload"]
        fitID = self.mainFrame.getActiveFit()
        sFit.refreshFit(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    @property
    def checked(self):
        sFit = Fit.getInstance()
        return sFit.serviceFittingOptions["useGlobalForceReload"]


FactorReload.register()
