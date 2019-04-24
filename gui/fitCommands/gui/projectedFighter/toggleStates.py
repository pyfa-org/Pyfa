import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.toggleState import CalcToggleFighterStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleProjectedFighterStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions):
        wx.Command.__init__(self, True, 'Toggle Projected Fighter States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions

    def Do(self):
        cmd = CalcToggleFighterStatesCommand(
            fitID=self.fitID,
            projected=True,
            mainPosition=self.mainPosition,
            positions=self.positions)
        success = self.internalHistory.submit(cmd)
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
