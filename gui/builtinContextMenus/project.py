from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.builtinViews.fittingView
import wx

class Project(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        if context not in ("item", "itemSearch") or self.mainFrame.getActiveFit() is None:
            return False

        item = selection[0]
        return item.isType("projected")

    def getText(self, context, selection):
        return "Project onto Fit"

    def activate(self, context, selection, i):
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.project(fitID, selection[0])
        wx.PostEvent(self.mainFrame, gui.builtinViews.fittingView.FitChanged(fitID=fitID))

Project.register()
