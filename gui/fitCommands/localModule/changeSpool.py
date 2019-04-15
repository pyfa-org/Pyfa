import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.module.changeSpool import CalcChangeModuleSpoolCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalModuleSpoolCommand(wx.Command):

    def __init__(self, fitID, position, spoolType, spoolAmount):
        wx.Command.__init__(self, True, 'Change Local Module Spool')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount

    def Do(self):
        cmd = CalcChangeModuleSpoolCommand(
            fitID=self.fitID,
            projected=False,
            position=self.position,
            spoolType=self.spoolType,
            spoolAmount=self.spoolAmount)
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
