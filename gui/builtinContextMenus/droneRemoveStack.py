from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
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
        srcContext = fullContext[0]
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit = sFit.getFit(fitID)

        idx = sFit.drones.index(selection[0])
        sFit.removeDrone(fitID, idx, numDronesToRemove=sFit.drones[idx].amount)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

ItemRemove.register()
