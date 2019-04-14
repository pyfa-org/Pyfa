import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.module.changeSpool import CalcChangeModuleSpoolCommand


class GuiSetSpoolup(wx.Command):

    def __init__(self, fitID, position, spoolType, spoolAmount, context):
        wx.Command.__init__(self, True, "Booster Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position
        self.spoolType = spoolType
        self.spoolupAmount = spoolAmount
        self.context = context

    def Do(self):
        if self.internal_history.Submit(CalcChangeModuleSpoolCommand(
            fitID=self.fitID,
            position=self.position,
            spoolType=self.spoolType,
            spoolAmount=self.spoolupAmount,
            projected=True if self.context == 'projectedModule' else False
        )):
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
