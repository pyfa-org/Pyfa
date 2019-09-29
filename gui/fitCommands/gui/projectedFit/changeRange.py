import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.projectedFit.changeProjectionRange import CalcChangeProjectedFitProjectionRangeCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedFitRangeCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Fit Projection Range')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.projectionRange = projectionRange

    def Do(self):
        cmd = CalcChangeProjectedFitProjectionRangeCommand(fitID=self.fitID, projectedFitID=self.projectedFitID, projectionRange=self.projectionRange)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        if cmd.needsGuiRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
