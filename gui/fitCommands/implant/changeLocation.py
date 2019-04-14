import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.implant.changeLocation import CalcChangeImplantLocationCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeImplantLocation(wx.Command):

    def __init__(self, fitID, source):
        wx.Command.__init__(self, True, 'Change Implant Location')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.source = source

    def Do(self):
        if self.internalHistory.submit(CalcChangeImplantLocationCommand(fitID=self.fitID, source=self.source)):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
