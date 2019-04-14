import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calcCommands.module.localChangeStates import CalcChangeLocalModuleStatesCommand


class GuiModuleStateChangeCommand(wx.Command):
    def __init__(self, fitID, baseMod, modules, click):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.fitID = fitID
        self.baseMod = baseMod
        self.modules = modules
        self.click = click
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        if self.internalHistory.Submit(CalcChangeLocalModuleStatesCommand(self.fitID, self.baseMod, self.modules, self.click)):
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
