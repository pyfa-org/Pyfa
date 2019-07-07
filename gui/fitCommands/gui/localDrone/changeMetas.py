import math

import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalDroneMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Local Drone Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        results = []
        for position in sorted(self.positions, reverse=True):
            drone = fit.drones[position]
            if drone.itemID == self.newItemID:
                continue
            info = DroneInfo.fromDrone(drone)
            info.itemID = self.newItemID
            cmdRemove = CalcRemoveLocalDroneCommand(
                fitID=self.fitID,
                position=position,
                amount=math.inf)
            cmdAdd = CalcAddLocalDroneCommand(
                fitID=self.fitID,
                droneInfo=info,
                forceNewStack=True,
                ignoreRestrictions=True)
            results.append(self.internalHistory.submitBatch(cmdRemove, cmdAdd))
        success = any(results)
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
