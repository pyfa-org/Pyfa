import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.fighter.localRemove import CalcRemoveLocalFighterCommand


class GuiRemoveFighterCommand(wx.Command):
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Fighter Remove")
        self.fitID = fitID
        self.position = position
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        success = self.internalHistory.Submit(CalcRemoveLocalFighterCommand(self.fitID, self.position))
        if success:
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
