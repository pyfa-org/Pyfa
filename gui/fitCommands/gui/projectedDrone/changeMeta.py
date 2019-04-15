import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedAdd import CalcAddProjectedDroneCommand
from gui.fitCommands.calc.drone.projectedRemove import CalcRemoveProjectedDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedDroneMetaCommand(wx.Command):

    def __init__(self, fitID, itemID, newItemID):
        wx.Command.__init__(self, True, 'Change Projected Drone Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.itemID), None)
        if drone is None:
            return False
        if drone.itemID == self.newItemID:
            return False
        info = DroneInfo.fromDrone(drone)
        info.itemID = self.newItemID
        cmdRemove = CalcRemoveProjectedDroneCommand(fitID=self.fitID, itemID=self.itemID, amount=math.inf)
        cmdAdd = CalcAddProjectedDroneCommand(fitID=self.fitID, droneInfo=info)
        success = self.internalHistory.submitBatch(cmdRemove, cmdAdd)
        sFit.recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
