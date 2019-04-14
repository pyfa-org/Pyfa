import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import FighterInfo
from service.fit import Fit
from .calcCommands.fighter.localAdd import CalcAddLocalFighterCommand


class GuiAddFighterCommand(wx.Command):
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Fighter Add")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        if self.internalHistory.Submit(CalcAddLocalFighterCommand(fitID=self.fitID, fighterInfo=FighterInfo(itemID=self.itemID))):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
