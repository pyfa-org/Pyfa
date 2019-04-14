import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.fighter.toggleState import CalcToggleFighterStateCommand


class GuiToggleFighterCommand(wx.Command):
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position

    def Do(self):
        if self.internalHistory.Submit(CalcToggleFighterStateCommand(self.fitID, False, self.position)):
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
