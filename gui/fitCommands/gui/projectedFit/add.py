import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.projectedFit.add import CalcAddProjectedFitCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiAddProjectedFitsCommand(wx.Command):

    def __init__(self, fitID, projectedFitIDs, amount):
        wx.Command.__init__(self, True, 'Add Projected Fits')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.projectedFitIDs = projectedFitIDs
        self.amount = amount

    def Do(self):
        results = []
        for projectedFitID in self.projectedFitIDs:
            cmd = CalcAddProjectedFitCommand(fitID=self.fitID, projectedFitID=projectedFitID, amount=self.amount)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
        sFit = Fit.getInstance()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
