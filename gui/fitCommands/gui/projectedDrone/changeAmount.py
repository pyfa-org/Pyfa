import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedChangeAmount import CalcChangeProjectedDroneAmountCommand
from gui.fitCommands.calc.drone.projectedRemove import CalcRemoveProjectedDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedDroneAmountCommand(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Change Projected Drone Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeProjectedDroneAmountCommand(fitID=self.fitID, itemID=self.itemID, amount=self.amount)
            if self.internalHistory.submit(cmd):
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        else:
            cmd = CalcRemoveProjectedDroneCommand(fitID=self.fitID, droneInfo=DroneInfo(itemID=self.itemID, amount=math.inf, amountActive=math.inf))
            if self.internalHistory.submit(cmd):
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
