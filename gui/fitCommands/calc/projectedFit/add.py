import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, amount=None, state=None):
        wx.Command.__init__(self, True, 'Add Projected Fit')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.amount = amount
        self.state = state

    def Do(self):
        pyfalog.debug('Doing addition of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        projectedFit = sFit.getFit(self.projectedFitID, projected=True)

        # Projected fit could have been deleted if we are redoing
        if projectedFit is None:
            pyfalog.debug('Projected fit is not available')
            return False

        if projectedFit in fit.projectedFits:
            pyfalog.debug('Projected fit had been applied already')
            return False

        if projectedFit.ID in fit.projectedFitDict:
            pyfalog.debug('Projected fit is in projected dict already')
            return False
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

        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected fit {} for fit {}'.format(self.projectedFitID, self.fitID))
        # Can't find the projected fit, it must have been deleted. Just skip, as deleted fit
        # means that someone else just did exactly what we wanted to do
        projectedFit = Fit.getInstance().getFit(self.projectedFitID, projected=True)
        if projectedFit is None:
            return True
        from .remove import CalcRemoveProjectedFitCommand
        cmd = CalcRemoveProjectedFitCommand(fitID=self.fitID, projectedFitID=self.projectedFitID)
        return cmd.Do()
