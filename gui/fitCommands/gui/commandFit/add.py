import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandFit.add import CalcAddCommandCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiAddCommandFitCommand(wx.Command):

    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True, 'Add Command Fit')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.commandFitID = commandFitID

    def Do(self):
        cmd = CalcAddCommandCommand(fitID=self.fitID, commandFitID=self.commandFitID)
        success = self.internalHistory.submit(cmd)
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
