import wx
from logbook import Logger

from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount):
        wx.Command.__init__(self, True, 'Add Projected Fit')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount
        self.savedState = None
        self.savedAmount = None
        self.changeAmountCommand = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing removal of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        projectedFit = sFit.getFit(self.projectedFitID, projected=True)

        # Can be removed by the time we're redoing it
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False
        projectionInfo = projectedFit.getProjectionInfo(self.fitID)
        if not projectionInfo:
            pyfalog.warning('Fit projection info is not available')
            return False

        self.savedState = projectionInfo.active
        self.savedAmount = projectionInfo.amount

        remainingAmount = projectionInfo.amount - self.amount

        # Change amount if more than 0 remaining, remove otherwise
        if remainingAmount > 0:
            from .changeAmount import CalcChangeProjectedFitAmountCommand
            self.changeAmountCommand = CalcChangeProjectedFitAmountCommand(
                fitID=self.fitID,
                projectedFitID=self.projectedFitID,
                amount=remainingAmount)
            if not self.changeAmountCommand.Do():
                return False
            sFit.recalc(fit)
            self.savedStateCheckChanges = sFit.checkStates(fit, None)
            return True
        else:
            self.changeAmountCommand = None
            if projectedFit.ID not in fit.projectedFitDict:
                pyfalog.warning('Unable to find projected fit in projected dict')
                return False
            del fit.projectedFitDict[projectedFit.ID]
            sFit.recalc(fit)
            self.savedStateCheckChanges = sFit.checkStates(fit, None)
            return True

    def Undo(self):
        pyfalog.debug('Undoing removal of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        if self.changeAmountCommand is not None:
            if not self.changeAmountCommand.Undo():
                return False
            restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
            return True
        from .add import CalcAddProjectedFitCommand
        cmd = CalcAddProjectedFitCommand(
            fitID=self.fitID,
            projectedFitID=self.projectedFitID,
            amount=self.savedAmount,
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
