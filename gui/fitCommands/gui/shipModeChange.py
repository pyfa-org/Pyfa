import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import InternalCommandHistory
from gui.fitCommands.calc.shipModeChange import CalcChangeShipModeCommand


class GuiChangeShipModeCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Change Ship Mode')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        cmd = CalcChangeShipModeCommand(fitID=self.fitID, itemID=self.itemID)
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
