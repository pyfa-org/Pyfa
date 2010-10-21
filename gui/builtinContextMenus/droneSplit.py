from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import gui.fittingView
import service
import wx

class DroneSplit(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("drone") and selection[0].amount > 1

    def getText(self, context, selection):
        return "Split stack"

    def activate(self, context, selection, i):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.splitDroneStack(fitID, selection[0], 1)
        wx.PostEvent(self.mainFrame, gui.fittingView.FitChanged(fitID=fitID))

DroneSplit.register()
