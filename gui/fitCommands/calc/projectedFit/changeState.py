import wx
from logbook import Logger

from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFitStateCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, state):
        wx.Command.__init__(self, True, 'Change Projected Fit State')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.state = state
        self.savedState = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing changing of projected fit {} state to {} for fit {}'.format(
            self.projectedFitID, self.state, self.fitID))
        sFit = Fit.getInstance()
        projectedFit = sFit.getFit(self.projectedFitID, projected=True)
        # Projected fit could have been deleted if we are redoing
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False
        projectionInfo = projectedFit.getProjectionInfo(self.fitID)
        if projectionInfo is None:
            pyfalog.warning('Fit projection info is not available')
            return False
        self.savedState = projectionInfo.active

        if self.state == self.savedState:
            return False

        projectionInfo.active = self.state

        fit = sFit.getFit(self.fitID)
        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, None)
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of projected fit {} state to {} for fit {}'.format(
            self.projectedFitID, self.state, self.fitID))
        cmd = CalcChangeProjectedFitStateCommand(
            fitID=self.fitID,
            projectedFitID=self.projectedFitID,
            state=self.savedState)
        if not cmd.Do():
            return False
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        return True

    @property
    def needsGuiRecalc(self):
        if self.savedStateCheckChanges is None:
            return True
        for container in self.savedStateCheckChanges:
            if len(container) > 0:
                return True
        return False
