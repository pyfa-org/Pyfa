import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.fighter.abilityToggleState import CalcToggleFighterAbilityStateCommand


class GuiToggleFighterAbilityCommand(wx.Command):

    def __init__(self, fitID, position, effectID, isProjected):
        wx.Command.__init__(self, True, "")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position
        self.effectID = effectID
        self.isProjected = isProjected

    def Do(self):
        if self.internalHistory.Submit(CalcToggleFighterAbilityStateCommand(self.fitID, self.isProjected, self.position, self.effectID)):
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
