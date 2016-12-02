from gui.contextMenu import ContextMenu
import gui.mainFrame
import wx
import gui.globalEvents as GE

class ItemRemove(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext == "droneItem"

    def getText(self, itmContext, selection):
        return "Remove {0} Stack".format(itmContext)

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        idx = fit.drones.index(selection[0])
        sFit.removeDrone(fitID, idx, numDronesToRemove=fit.drones[idx].amount)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

ItemRemove.register()
