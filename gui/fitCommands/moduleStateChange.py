import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .fitChangeState import FitChangeStatesCommand

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
        # todo: determine if we've changed state (recalc). If not, store that so we don't attempt to recalc on undo
        self.internal_history.Submit(FitChangeStatesCommand(self.fitID, self.baseMod, self.modules, self.click))
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for x in self.internal_history.Commands:
            self.internal_history.Undo()
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

