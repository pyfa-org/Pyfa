import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.abilityToggleStates import CalcToggleFighterAbilityStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleLocalFighterAbilityStateCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions, effectID):
        wx.Command.__init__(self, True, 'Toggle Local Fighter Ability State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions
        self.effectID = effectID

    def Do(self):
        cmd = CalcToggleFighterAbilityStatesCommand(
            fitID=self.fitID,
            projected=False,
            mainPosition=self.mainPosition,
            positions=self.positions,
            effectID=self.effectID)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
