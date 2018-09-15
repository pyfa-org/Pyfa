import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitChangeState import FitChangeStatesCommand


class GuiModuleStateChangeCommand(wx.Command):
    def __init__(self, fitID, baseMod, modules, click):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.baseMod = baseMod
        self.modules = modules
        self.click = click
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        if self.internal_history.Submit(FitChangeStatesCommand(self.fitID, self.baseMod, self.modules, self.click)):
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
