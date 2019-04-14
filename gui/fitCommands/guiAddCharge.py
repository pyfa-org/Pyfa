import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.module.changeCharges import CalcChangeModuleChargesCommand


class GuiModuleAddChargeCommand(wx.Command):
    def __init__(self, fitID, itemID, modules):
        wx.Command.__init__(self, True, "Module Charge Add")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.positions = [mod.modPosition for mod in modules]
        self.projected = modules[0].isProjected

    def Do(self):
        if self.internalHistory.Submit(CalcChangeModuleChargesCommand(self.fitID, {p: self.itemID for p in self.positions}, self.projected)):
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
