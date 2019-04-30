import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.changeLocation import CalcChangeImplantLocationCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeImplantLocationCommand(wx.Command):

    def __init__(self, fitID, source):
        wx.Command.__init__(self, True, 'Change Implant Location')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.source = source

    def Do(self):
        cmd = CalcChangeImplantLocationCommand(fitID=self.fitID, source=self.source)
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
