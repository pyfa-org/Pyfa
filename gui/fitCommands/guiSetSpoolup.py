import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitSetSpoolup import FitSetSpoolupCommand


class GuiSetSpoolup(wx.Command):
    def __init__(self, fitID, module, spoolupType, spoolupAmount):
        wx.Command.__init__(self, True, "Booster Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.position = module.modPosition
        self.spoolType = spoolupType
        self.spoolupAmount = spoolupAmount

    def Do(self):
        if self.internal_history.Submit(FitSetSpoolupCommand(self.fitID, self.position, self.spoolType, self.spoolupAmount)):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
