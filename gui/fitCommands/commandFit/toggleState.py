import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.commandFit.toggleState import CalcToggleCommandFitStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleCommandFitStateCommand(wx.Command):

    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True, 'Toggle Command Fit State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.commandFitID = commandFitID

    def Do(self):
        if self.internalHistory.submit(CalcToggleCommandFitStateCommand(fitID=self.fitID, commandFitID=self.commandFitID)):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
