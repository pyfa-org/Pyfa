import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import CargoInfo
from .calc.cargo.add import FitAddCargoCommand


class GuiAddCargoCommand(wx.Command):

    def __init__(self, fitID, itemID, amount=1):
        wx.Command.__init__(self, True, "Cargo Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        if self.internal_history.Submit(FitAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=self.amount))):
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
