import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.module.projectedChangeState import CalcChangeProjectedModuleStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedModuleStateCommand(wx.Command):

    def __init__(self, fitID, position, click):
        wx.Command.__init__(self, True, 'Change Projected Module State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.click = click

    def Do(self):
        cmd = CalcChangeProjectedModuleStateCommand(fitID=self.fitID, position=self.position, click=self.click)
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
