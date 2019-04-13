import wx
import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitChangeCargoAmount import FitChangeCargoAmount
from service.fit import Fit
from gui.fitCommands.helpers import CargoInfo
from logbook import Logger
pyfalog = Logger(__name__)


class GuiChangeCargoQty(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, "")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        cmd = FitChangeCargoAmount(self.fitID, CargoInfo(itemID=self.itemID, amount=self.amount))
        if self.internal_history.Submit(cmd):
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
