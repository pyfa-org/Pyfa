import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandFit.toggleStates import CalcToggleCommandFitStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleCommandFitStatesCommand(wx.Command):

    def __init__(self, fitID, mainCommandFitID, commandFitIDs):
        wx.Command.__init__(self, True, 'Toggle Command Fit States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainCommandFitID = mainCommandFitID
        self.commandFitIDs = commandFitIDs

    def Do(self):
        cmd = CalcToggleCommandFitStatesCommand(
            fitID=self.fitID,
            mainCommandFitID=self.mainCommandFitID,
            commandFitIDs=self.commandFitIDs)
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
