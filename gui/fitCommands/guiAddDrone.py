import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitAddDrone import FitAddDroneCommand


class GuiAddDroneCommand(wx.Command):
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Cargo Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        cmd = FitAddDroneCommand(self.fitID, self.itemID)
        if self.internal_history.Submit(cmd):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
