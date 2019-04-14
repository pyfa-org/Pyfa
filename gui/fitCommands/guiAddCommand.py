import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.commandFit.add import CalcAddCommandCommand


class GuiAddCommandCommand(wx.Command):
    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True, "")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.commandFitID = commandFitID

    def Do(self):
        if self.internalHistory.Submit(CalcAddCommandCommand(self.fitID, self.commandFitID, None)):
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            Fit.getInstance().recalc(self.fitID)
            return True
        return False

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
