import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.projectedFit.remove import CalcRemoveProjectedFitCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiRemoveProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID):
        wx.Command.__init__(self, True, 'Remove Projected Fit')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.projectedFitID = projectedFitID

    def Do(self):
        cmd = CalcRemoveProjectedFitCommand(fitID=self.fitID, projectedFitID=self.projectedFitID)
        if self.internalHistory.submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
