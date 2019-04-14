import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.drone.localRemove import CalcRemoveLocalDroneCommand


class GuiRemoveDroneCommand(wx.Command):
    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True, "Drone Remove")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position
        self.amount = amount

    def Do(self):
        cmd = CalcRemoveLocalDroneCommand(self.fitID, self.position, self.amount)
        if self.internalHistory.Submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
