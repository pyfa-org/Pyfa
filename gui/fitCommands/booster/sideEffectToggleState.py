import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.booster.sideEffectToggleState import CalcToggleBoosterSideEffectStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleBoosterSideEffectStateCommand(wx.Command):

    def __init__(self, fitID, position, effectID):
        wx.Command.__init__(self, True, 'Toggle Booster Side Effect State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.effectID = effectID

    def Do(self):
        if self.internalHistory.submit(CalcToggleBoosterSideEffectStateCommand(fitID=self.fitID, position=self.position, effectID=self.effectID)):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
