import wx
import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.cargo.changeAmount import CalcChangeCargoAmountCommand
from service.fit import Fit
from gui.fitCommands.helpers import CargoInfo
from logbook import Logger
pyfalog = Logger(__name__)


class GuiChangeCargoQty(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, "")
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        cmd = CalcChangeCargoAmountCommand(self.fitID, CargoInfo(itemID=self.itemID, amount=self.amount))
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
