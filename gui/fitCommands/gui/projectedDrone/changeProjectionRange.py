import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedChangeProjectionRange import CalcChangeProjectedDroneProjectionRangeCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedDroneProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, itemID, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Drone Projection Range')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.projectionRange = projectionRange

    def Do(self):
        cmd = CalcChangeProjectedDroneProjectionRangeCommand(
            fitID=self.fitID,
            itemID=self.itemID,
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
