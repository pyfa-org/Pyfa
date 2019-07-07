import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiSplitLocalDroneStackCommand(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Split Local Drone Stack')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.amount = amount

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        drone = fit.drones[self.position]
        if self.amount >= drone.amount:
            return False
        info = DroneInfo.fromDrone(drone)
        info.amount = self.amount
        info.amountActive = min(self.amount, info.amountActive)
        commands = []
        commands.append(CalcRemoveLocalDroneCommand(
            fitID=self.fitID,
            position=self.position,
            amount=self.amount))
        commands.append(CalcAddLocalDroneCommand(
            fitID=self.fitID,
            droneInfo=info,
            forceNewStack=True,
            ignoreRestrictions=True))
        success = self.internalHistory.submitBatch(*commands)
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
