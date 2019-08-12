import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount, state=None):
        wx.Command.__init__(self, True, 'Add Projected Fit')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount
        self.state = state
        self.changeAmountCommand = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing addition of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        projectedFit = sFit.getFit(self.projectedFitID, projected=True)

        # Projected fit could have been deleted if we are redoing
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False

        # If we already have info about projection - means that fit is already projected
        # and we just need to increase amount of fits
        if projectedFit in fit.projectedFits and projectedFit.ID in fit.projectedFitDict:
            from .changeAmount import CalcChangeProjectedFitAmountCommand
            self.changeAmountCommand = CalcChangeProjectedFitAmountCommand(
                fitID=self.fitID,
                projectedFitID=self.projectedFitID,
                amount=self.amount,
                relative=True)
            if not self.changeAmountCommand.Do():
                return False
            sFit.recalc(fit)
            self.savedStateCheckChanges = sFit.checkStates(fit, None)
            return True
        else:
            self.changeAmountCommand = None

        fit.projectedFitDict[projectedFit.ID] = projectedFit
        # This bit is required, see issue #83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(projectedFit)

        if self.amount is not None or self.state is not None:
            projectionInfo = projectedFit.getProjectionInfo(self.fitID)
            if projectionInfo is None:
                pyfalog.warning('Fit projection info is not available')
                self.Undo()
                return False
            if self.amount is not None:
                projectionInfo.amount = self.amount
            if self.state is not None:
                projectionInfo.active = self.state

        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, None)
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        if self.changeAmountCommand is not None:
            if not self.changeAmountCommand.Undo():
                return False
            restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
            return True
        # Can't find the projected fit, it must have been deleted. Just skip, as deleted fit
        # means that someone else just did exactly what we wanted to do
        projectedFit = Fit.getInstance().getFit(self.projectedFitID, projected=True)
        if projectedFit is not None:
            from .remove import CalcRemoveProjectedFitCommand
            cmd = CalcRemoveProjectedFitCommand(
                fitID=self.fitID,
                projectedFitID=self.projectedFitID,
                amount=self.amount)
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
