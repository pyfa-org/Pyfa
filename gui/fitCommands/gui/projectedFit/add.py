import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.projectedFit.add import CalcAddProjectedFitCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiAddProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount):
        wx.Command.__init__(self, True, 'Add Projected Fit')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount

    def Do(self):
        cmd = CalcAddProjectedFitCommand(fitID=self.fitID, projectedFitID=self.projectedFitID, amount=self.amount)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
