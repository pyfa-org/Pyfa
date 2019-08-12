import wx
from logbook import Logger

from eos.const import FittingModuleState
from eos.saveddata.module import Module
from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


STATE_MAP = {
    'inactive': FittingModuleState.OFFLINE,
    'active': FittingModuleState.ACTIVE,
    'overheat': FittingModuleState.OVERHEATED}


class CalcChangeProjectedModuleStatesCommand(wx.Command):

    def __init__(self, fitID, positions, proposedState):
        wx.Command.__init__(self, True, 'Change Projected Module States')
        self.fitID = fitID
        self.positions = positions
        self.proposedState = STATE_MAP[proposedState]
        self.savedStates = {}
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing change of projected module state at positions {} to state {} on fit {}'.format(
            self.positions, self.proposedState, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        self.savedStates = {pos: fit.projectedModules[pos].state for pos in self.positions}

        changed = False
        for position in self.positions:
            mod = fit.projectedModules[position]
            proposedState = Module.getProposedState(mod, None, self.proposedState)
            if proposedState != mod.state:
                pyfalog.debug('Toggle projected {} state: {} for fit ID: {}'.format(mod, proposedState, self.fitID))
                mod.state = proposedState
                changed = True
        if not changed:
            return False
        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, None)
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected module state at positions {} to state {} on fit {}'.format(
            self.positions, self.proposedState, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        for position, state in self.savedStates.items():
            mod = fit.projectedModules[position]
            pyfalog.debug('Reverting projected {} to state {} for fit ID {}'.format(mod, state, self.fitID))
            mod.state = state
        restoreCheckedStates(fit, self.savedStateCheckChanges)
        return True

    @property
    def needsGuiRecalc(self):
        if self.savedStateCheckChanges is None:
            return True
        for container in self.savedStateCheckChanges:
            if len(container) > 0:
                return True
        return False
