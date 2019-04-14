import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.booster.add import CalcAddBoosterCommand
from gui.fitCommands.helpers import BoosterInfo, InternalCommandHistory
from service.fit import Fit


class GuiAddBoosterCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Add Booster')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        cmd = CalcAddBoosterCommand(fitID=self.fitID, boosterInfo=BoosterInfo(itemID=self.itemID))
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
