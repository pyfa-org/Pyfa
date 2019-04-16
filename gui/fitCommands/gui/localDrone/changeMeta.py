import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalDroneMetaCommand(wx.Command):

    def __init__(self, fitID, position, newItemID):
        wx.Command.__init__(self, True, 'Change Local Drone Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        drone = fit.drones[self.position]
        if drone.itemID == self.newItemID:
            return False
        info = DroneInfo.fromDrone(drone)
        info.itemID = self.newItemID
        cmdRemove = CalcRemoveLocalDroneCommand(fitID=self.fitID, position=self.position, amount=math.inf)
        cmdAdd = CalcAddLocalDroneCommand(fitID=self.fitID, droneInfo=info, forceNewStack=True)
        success = self.internalHistory.submitBatch(cmdRemove, cmdAdd)
        sFit.recalc(fit)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
