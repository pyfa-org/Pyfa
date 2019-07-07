import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiCloneLocalDroneCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Clone Local Drone')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        try:
            drone = fit.drones[self.position]
        except IndexError:
            return False
        info = DroneInfo.fromDrone(drone)
        cmd = CalcAddLocalDroneCommand(fitID=self.fitID, droneInfo=info, forceNewStack=True)
        success = self.internalHistory.submit(cmd)
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
