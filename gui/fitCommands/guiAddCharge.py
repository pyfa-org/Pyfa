import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.module.changeCharges import FitChangeModuleChargesCommand


class GuiModuleAddChargeCommand(wx.Command):
    def __init__(self, fitID, itemID, modules):
        wx.Command.__init__(self, True, "Module Charge Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.positions = [mod.modPosition for mod in modules]
        self.projected = modules[0].isProjected

    def Do(self):
        if self.internal_history.Submit(FitChangeModuleChargesCommand(self.fitID, {p: self.itemID for p in self.positions}, self.projected)):
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
