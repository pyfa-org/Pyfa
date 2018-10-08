import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitAddCargo import FitAddCargoCommand


class GuiAddCargoCommand(wx.Command):
    def __init__(self, fitID, itemID, amount=1, replace=False):
        wx.Command.__init__(self, True, "Cargo Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount
        self.replace = replace

    def Do(self):
        if self.internal_history.Submit(FitAddCargoCommand(self.fitID, self.itemID, self.amount, self.replace)):
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
