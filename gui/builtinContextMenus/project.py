from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.globalEvents as GE
import wx

class Project(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        item = selection[0]
        return item.isType("projected")

    def getText(self, itmContext, selection):
        return "Project {0} onto Fit".format(itmContext)

    def activate(self, fullContext, selection, i):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.project(fitID, selection[0])
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

Project.register()
