import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.toggleState import CalcToggleFighterStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleLocalFighterStateCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Toggle Local Fighter State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position

    def Do(self):
        cmd = CalcToggleFighterStateCommand(fitID=self.fitID, projected=False, position=self.position)
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
