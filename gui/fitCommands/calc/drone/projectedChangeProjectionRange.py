import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedDroneProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, itemID, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Drone Projection Range')
        self.fitID = fitID
        self.itemID = itemID
        self.projectionRange = projectionRange
        self.savedProjectionRange = None

    def Do(self):
        pyfalog.debug('Doing change of projected drone {} projection range to {} on fit {}'.format(
            self.itemID, self.projectionRange, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.itemID), None)
        if drone is None:
            pyfalog.warning('Cannot find projected drone')
            return False
        if drone.projectionRange == self.projectionRange:
            return False
        self.savedProjectionRange = drone.projectionRange
        drone.projectionRange = self.projectionRange
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected drone {} projection range to {} on fit {}'.format(
            self.itemID, self.projectionRange, self.fitID))
        cmd = CalcChangeProjectedDroneProjectionRangeCommand(
            fitID=self.fitID,
            itemID=self.itemID,
            projectionRange=self.savedProjectionRange)
        return cmd.Do()
