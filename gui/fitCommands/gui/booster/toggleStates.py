import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.booster.toggleStates import CalcToggleBoosterStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleBoosterStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions):
        wx.Command.__init__(self, True, 'Toggle Booster States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions

    def Do(self):
        cmd = CalcToggleBoosterStatesCommand(fitID=self.fitID, mainPosition=self.mainPosition, positions=self.positions)
        success = self.internalHistory.submit(cmd)
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
