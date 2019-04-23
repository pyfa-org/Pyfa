# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from service.fit import Fit
from service.settings import ContextMenuSettings


class FactorReload(ContextMenuCombined):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        return srcContext == "firepowerViewFull"

    @property
    def enabled(self):
        return self.mainFrame.getActiveFit() is not None

    def getText(self, itmContext, mainItem, selection):
        return "Factor in Reload Time"

    def activate(self, fullContext, mainItem, selection, i):
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
