import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFitAmountCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount, relative=False):
        wx.Command.__init__(self, True, 'Change Projected Fit Amount')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount
        self.relative = relative
        self.savedAmount = None

    def Do(self):
        pyfalog.debug('Doing change of projected fit {} amount to {} for fit {}'.format(self.projectedFitID, self.amount, self.fitID))
        projectedFit = Fit.getInstance().getFit(self.projectedFitID, projected=True)
        # Projected fit could have been deleted if we are redoing
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False
        projectionInfo = projectedFit.getProjectionInfo(self.fitID)
        if projectionInfo is None:
            pyfalog.warning('Fit projection info is not available')
            return False
        self.savedAmount = projectionInfo.amount
        if self.relative:
            amount = projectionInfo.amount + self.amount
        else:
            amount = self.amount
        # Limit to [1, 20]
        confinedAmount = min(20, max(1, amount))
        if confinedAmount == self.savedAmount:
            return False
        projectionInfo.amount = confinedAmount
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected fit {} amount to {} for fit {}'.format(self.projectedFitID, self.amount, self.fitID))
        cmd = CalcChangeProjectedFitAmountCommand(
            fitID=self.fitID,
            projectedFitID=self.projectedFitID,
            amount=self.savedAmount)
        return cmd.Do()
