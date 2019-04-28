import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFitStateCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, state, commit=True):
        wx.Command.__init__(self, True, 'Change Projected Fit State')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.state = state
        self.commit = commit
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing changing of projected fit {} state to {} for fit {}'.format(
            self.projectedFitID, self.state, self.fitID))
        projectedFit = Fit.getInstance().getFit(self.projectedFitID, projected=True)
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

        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of projected fit {} state to {} for fit {}'.format(
            self.projectedFitID, self.state, self.fitID))
        cmd = CalcChangeProjectedFitStateCommand(
            fitID=self.fitID,
            projectedFitID=self.projectedFitID,
            state=self.savedState,
            commit=self.commit)
        return cmd.Do()
