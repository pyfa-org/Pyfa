import math

import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiRevertMutatedLocalDroneCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Revert Local Drone from Mutated')
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
        if not drone.isMutated:
            return False
        info = DroneInfo(
            amount=drone.amount,
            amountActive=drone.amountActive,
            itemID=drone.baseItemID)
        cmdRemove = CalcRemoveLocalDroneCommand(
            fitID=self.fitID,
            position=self.position,
            amount=math.inf)
        cmdAdd = CalcAddLocalDroneCommand(
            fitID=self.fitID,
            droneInfo=info,
            forceNewStack=True,
            ignoreRestrictions=True)
        success = self.internalHistory.submitBatch(cmdRemove, cmdAdd)
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
