import wx
from logbook import Logger

from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFitProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Fit Projection Range')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.projectionRange = projectionRange
        self.savedProjectionRange = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing change of projected fit {} range to {} for fit {}'.format(self.projectedFitID, self.projectionRange, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        projectedFit = sFit.getFit(self.projectedFitID, projected=True)
        # Projected fit could have been deleted if we are redoing
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False
        projectionInfo = projectedFit.getProjectionInfo(self.fitID)
        if projectionInfo is None:
            pyfalog.warning('Fit projection info is not available')
            return False
        if projectionInfo.projectionRange == self.projectionRange:
            return False
        self.savedProjectionRange = projectionInfo.projectionRange
        projectionInfo.projectionRange = self.projectionRange

        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, None)
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected fit {} range to {} for fit {}'.format(self.projectedFitID, self.projectionRange, self.fitID))
        cmd = CalcChangeProjectedFitProjectionRangeCommand(
            fitID=self.fitID,
            projectedFitID=self.projectedFitID,
            projectionRange=self.savedProjectionRange)
        result = cmd.Do()
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        return result

    @property
    def needsGuiRecalc(self):
        if self.savedStateCheckChanges is None:
            return True
        for container in self.savedStateCheckChanges:
            if len(container) > 0:
                return True
        return False
