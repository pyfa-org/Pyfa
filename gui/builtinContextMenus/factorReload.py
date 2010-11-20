from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.builtinViews.fittingView
import wx
from gui import bitmapLoader

class FactorReload(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("firepowerViewFull",) and self.mainFrame.getActiveFit() is not None

    def getText(self, context, selection):
        return "Factor in Reload Time"

    def activate(self, context, selection, i):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.toggleFactorReload(fitID)
        wx.PostEvent(self.mainFrame, gui.builtinViews.fittingView.FitChanged(fitID=fitID))

    def getBitmap(self, context, selection):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        if fit.factorReload:
            return bitmapLoader.getBitmap("state_active_small", "icons")
        else:
            return None


FactorReload.register()
