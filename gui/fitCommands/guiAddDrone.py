import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import DroneInfo
from .calcCommands.drone.localAdd import CalcAddLocalDroneCommand


class GuiAddDroneCommand(wx.Command):
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Drone Add")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        cmd = CalcAddLocalDroneCommand(fitID=self.fitID, droneInfo=DroneInfo(itemID=self.itemID, amount=1, amountActive=0))
        if self.internalHistory.Submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
