import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .fitSwapModule import FitSwapModuleCommand
from .fitCloneModule import FitCloneModduleCommand

class GuiModuleSwapOrCloneCommand(wx.Command):
    def __init__(self, fitID, srcPosition, dstPosition, clone=False):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.clone = clone
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        result = None
        if self.clone:
            result = self.internal_history.Submit(FitCloneModduleCommand(self.fitID, self.srcPosition, self.dstPosition))
        else:
            result = self.internal_history.Submit(FitSwapModuleCommand(self.fitID, self.srcPosition, self.dstPosition))

        if result:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return result

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
