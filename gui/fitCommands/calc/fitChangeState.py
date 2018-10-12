import wx
from logbook import Logger

import gui.mainFrame
from eos.saveddata.module import Module
from service.fit import Fit
import eos.db

pyfalog = Logger(__name__)


class FitChangeStatesCommand(wx.Command):
    """
    Fitting command that trys to change the state of modules in [positions]. We use the base module to determine the
    state that we will try to apply for all modules.


    """
    def __init__(self, fitID, baseModPos, positions, click):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.baseModPos = baseModPos
        self.positions = positions
        self.click = click
        self.changed = None
        self.old_states = {}

    def Do(self):
        fit = eos.db.getFit(self.fitID)
        sFit = Fit.getInstance()
        baseMod = fit.modules[self.baseModPos]

        # make sure positions only include non-empty positions
        self.positions = [x for x in self.positions if not fit.modules[x].isEmpty]

        for x in self.positions:
            self.old_states[x] = fit.modules[x].state

        proposedState = Module.getProposedState(baseMod, self.click)
        pyfalog.debug("Attempting to change modules to {}", proposedState)

        if proposedState != baseMod.state:
            pyfalog.debug("Toggle {} state: {} for fit ID: {}", baseMod, proposedState, self.fitID)

            self.changed = True
            baseMod.state = proposedState
            for i in [x for x in self.positions if x != self.baseModPos]:  # dont consider base module position
                mod = fit.modules[i]
                p = Module.getProposedState(mod, self.click, proposedState)
                mod.state = p
                if p != mod.state:
                    pyfalog.debug("Toggle {} state: {} for fit ID: {}", mod, p, self.fitID)
                    self.changed = True

        # if we haven't change the state (eg, overheat -> overheat), simply fail the command
        if self.changed:
            eos.db.commit()
            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            # self.recalc(fit)
            # # Then, check states of all modules and change where needed. This will recalc if needed
            sFit.checkStates(fit, baseMod)
            # self.checkStates(fit, base)
            return True
        return False

    def Undo(self):
        # todo: some sanity checking to make sure that we are applying state back to the same modules?
        fit = self.sFit.getFit(self.fitID)
        for k, v in self.old_states.items():
            mod = fit.modules[k]
            pyfalog.debug("Reverting {} to state {} for fit ID", mod, v, self.fitID)
            mod.state = v
        return True
