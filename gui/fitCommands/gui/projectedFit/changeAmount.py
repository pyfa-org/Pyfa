import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.projectedFit.changeAmount import CalcChangeProjectedFitAmountCommand
from gui.fitCommands.calc.projectedFit.remove import CalcRemoveProjectedFitCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedFitAmountCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount):
        wx.Command.__init__(self, True, 'Change Projected Fit Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeProjectedFitAmountCommand(fitID=self.fitID, projectedFitID=self.projectedFitID, amount=self.amount)
        else:
            cmd = CalcRemoveProjectedFitCommand(fitID=self.fitID, projectedFitID=self.projectedFitID, amount=math.inf)
        success = self.internalHistory.submit(cmd)
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
