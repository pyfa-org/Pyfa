# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit

_t = wx.GetTranslation


class FactorReload(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == "firepowerViewFull"

    @property
    def enabled(self):
        return self.mainFrame.getActiveFit() is not None

    def getText(self, callingWindow, itmContext):
        return _t("Factor in Reload Time")

    def activate(self, callingWindow, fullContext, i):
        fitIDs = Fit.getInstance().toggleFactorReload()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=tuple(fitIDs)))

    def isChecked(self, i):
        sFit = Fit.getInstance()
        return sFit.serviceFittingOptions["useGlobalForceReload"]


FactorReload.register()
