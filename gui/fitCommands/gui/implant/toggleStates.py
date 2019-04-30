import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.toggleStates import CalcToggleImplantStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleImplantStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions):
        wx.Command.__init__(self, True, 'Toggle Implant States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions

    def Do(self):
        cmd = CalcToggleImplantStatesCommand(fitID=self.fitID, mainPosition=self.mainPosition, positions=self.positions)
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
