import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitSetCharge import FitSetChargeCommand


class GuiModuleAddChargeCommand(wx.Command):
    def __init__(self, fitID, itemID, modules):
        wx.Command.__init__(self, True, "Module Charge Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.positions = [mod.modPosition for mod in modules]

    def Do(self):
        if self.internal_history.Submit(FitSetChargeCommand(self.fitID, self.positions, self.itemID)):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
