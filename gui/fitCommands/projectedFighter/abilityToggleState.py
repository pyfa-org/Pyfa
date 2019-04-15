import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.fighter.abilityToggleState import CalcToggleFighterAbilityStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleProjectedFighterAbilityStateCommand(wx.Command):

    def __init__(self, fitID, position, effectID):
        wx.Command.__init__(self, True, 'Toggle Projected Fighter Ability State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.effectID = effectID

    def Do(self):
        cmd = CalcToggleFighterAbilityStateCommand(fitID=self.fitID, projected=True, position=self.position, effectID=self.effectID)
        if self.internalHistory.submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
