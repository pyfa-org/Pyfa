import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.projectedChangeProjectionRange import CalcChangeProjectedModuleProjectionRangeCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedModuleProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, position, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Module Projection Range')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.projectionRange = projectionRange

    def Do(self):
        cmd = CalcChangeProjectedModuleProjectionRangeCommand(
            fitID=self.fitID,
            position=self.position,
            projectionRange=self.projectionRange)
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
