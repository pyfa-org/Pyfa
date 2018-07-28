import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from logbook import Logger
from eos.saveddata.module import Module
pyfalog = Logger(__name__)
import eos.db

class FitChangeStatesCommand(wx.Command):
    def __init__(self, fitID, baseMod, modules, click):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.baseMod = baseMod
        self.modules = modules
        self.click = click
        self.changed = None
        self.old_states = {}
        for mod in modules:
            # we don't use the actual module as the key, because it may have been deleted in subsequent calls (even if
            # we undo a deletion, wouldn't be the same obj). So, we store the position
            self.old_states[mod.modPosition] = mod.state

    def Do(self):
        # todo: determine if we've changed state (recalc). If not, store that so we don't attempt to recalc on undo
        # self.sFit.toggleModulesState(self.fitID, self.baseMod, self.modules, self.click)

        pyfalog.debug("Toggle module state for fit ID: {0}", self.fitID)
        changed = False
        proposedState = Module.getProposedState(self.baseMod, self.click)

        if proposedState != self.baseMod.state:
            changed = True
            self.baseMod.state = proposedState
            for mod in self.modules:
                if mod != self.baseMod:
                    p = Module.getProposedState(mod, self.click, proposedState)
                    mod.state = p
                    if p != mod.state:
                        changed = True

        if changed:
            self.changed = changed
            eos.db.commit()
            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            # self.recalc(fit)
            # # Then, check states of all modules and change where needed. This will recalc if needed
            # self.checkStates(fit, base)
            return True
        return False

    def Undo(self):
        # todo: some sanity checking to make sure that we are applying state back to the same modules?
        fit = self.sFit.getFit(self.fitID)
        for k, v in self.old_states.items():
            fit.modules[k].state = v
        return True
