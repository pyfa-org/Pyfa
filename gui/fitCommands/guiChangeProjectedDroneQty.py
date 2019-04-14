import wx
import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.drone.projectedChangeAmount import CalcChangeProjectedDroneAmountCommand
from service.fit import Fit
from logbook import Logger
pyfalog = Logger(__name__)


class GuiChangeProjectedDroneQty(wx.Command):
    def __init__(self, fitID, itemID, amount=1):
        wx.Command.__init__(self, True, "")
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        cmd = CalcChangeProjectedDroneAmountCommand(self.fitID, self.itemID, self.amount)
        if self.internalHistory.Submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
