import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.module.changeSpool import CalcChangeModuleSpoolCommand


class GuiSetSpoolup(wx.Command):

    def __init__(self, fitID, position, spoolType, spoolAmount, context):
        wx.Command.__init__(self, True, "Booster Add")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position
        self.spoolType = spoolType
        self.spoolupAmount = spoolAmount
        self.context = context

    def Do(self):
        if self.internalHistory.Submit(CalcChangeModuleSpoolCommand(
            fitID=self.fitID,
            position=self.position,
            spoolType=self.spoolType,
            spoolAmount=self.spoolupAmount,
            projected=True if self.context == 'projectedModule' else False
        )):
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
