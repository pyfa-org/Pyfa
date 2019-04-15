import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectedFitID, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Projected Fit State')
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of projected fit {} state for fit {}'.format(self.projectedFitID, self.fitID))
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
        projectionInfo.active = not projectionInfo.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of projected fit {} state for fit {}'.format(self.projectedFitID, self.fitID))
        cmd = CalcToggleProjectedFitCommand(fitID=self.fitID, projectedFitID=self.projectedFitID, forceState=self.savedState)
        return cmd.Do()
