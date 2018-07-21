import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE


class FitModuleStateChangeCommand(wx.Command):
    def __init__(self, fitID, baseMod, modules, click):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.baseMod = baseMod
        self.modules = modules
        self.click = click

        self.old_states = {}
        for mod in modules:
            # we don't use the actual module as the key, because it may have been deleted in subsequent calls (even if
            # we undo a deletion, wouldn't be the same obj). So, we store the position
            self.old_states[mod.modPosition] = mod.state

    def Do(self):
        # todo: determine if we've changed state (recalc). If not, store that so we don't attempt to recalc on undo
        self.sFit.toggleModulesState(self.fitID, self.baseMod, self.modules, self.click)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        # todo: some sanity checking to make sure that we are applying state back to the same modules?
        fit = self.sFit.getFit(self.fitID)
        for k, v in self.old_states.items():
            fit.modules[k].state = v
        self.sFit.recalc(fit)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
