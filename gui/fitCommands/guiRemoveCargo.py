import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitRemoveCargo import FitRemoveCargoCommand


class GuiRemoveCargoCommand(wx.Command):
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Module Charge Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        if self.internal_history.Submit(FitRemoveCargoCommand(self.fitID, self.itemID, stack=True)):
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.GetCommands():
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
