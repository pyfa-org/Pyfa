import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.projectedChangeProjectionRange import CalcChangeProjectedFighterProjectionRangeCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedFighterProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, position, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Fighter Projection Range')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.projectionRange = projectionRange

    def Do(self):
        cmd = CalcChangeProjectedFighterProjectionRangeCommand(
            fitID=self.fitID,
            position=self.position,
            projectionRange=self.projectionRange)
        success = self.internalHistory.submit(cmd)
        eos.db.flush()
        sFit = Fit.getInstance()
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
