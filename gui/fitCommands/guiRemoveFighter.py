import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitRemoveFighter import FitRemoveFighterCommand


class GuiRemoveFighterCommand(wx.Command):
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Module Remove")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.position = position
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        success = self.internal_history.Submit(FitRemoveFighterCommand(self.fitID, self.position))

        if success:
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
