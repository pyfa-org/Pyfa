import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import CargoInfo
from .calcCommands.cargo.add import CalcAddCargoCommand


class GuiAddCargoCommand(wx.Command):

    def __init__(self, fitID, itemID, amount=1):
        wx.Command.__init__(self, True, "Cargo Add")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        if self.internalHistory.Submit(CalcAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=self.amount))):
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
