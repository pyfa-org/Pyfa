import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount, commit=True):
        wx.Command.__init__(self, True, 'Add Projected Fit')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount
        self.commit = commit
        self.savedState = None
        self.savedAmount = None
        self.changeAmountCommand = None

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
                amount=remainingAmount,
                commit=self.commit)
            return self.changeAmountCommand.Do()
        else:
            self.changeAmountCommand = None
            if projectedFit.ID not in fit.projectedFitDict:
                pyfalog.warning('Unable to find projected fit in projected dict')
                return False
            del fit.projectedFitDict[projectedFit.ID]
            if self.commit:
                eos.db.commit()
            return True

    def Undo(self):
        pyfalog.debug('Undoing removal of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        if self.changeAmountCommand is not None:
            return self.changeAmountCommand.Undo()
        from .add import CalcAddProjectedFitCommand
        cmd = CalcAddProjectedFitCommand(
            fitID=self.fitID,
            projectedFitID=self.projectedFitID,
            amount=self.savedAmount,
            state=self.savedState,
            commit=self.commit)
        return cmd.Do()
