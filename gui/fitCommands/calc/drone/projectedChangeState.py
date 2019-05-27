import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedDroneStateCommand(wx.Command):

    def __init__(self, fitID, itemID, state):
        wx.Command.__init__(self, True, 'Change Projected Drone State')
        self.fitID = fitID
        self.itemID = itemID
        self.state = state
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing changing of projected drone {} state to {} for fit {}'.format(self.itemID, self.state, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.itemID), None)
        if drone is None:
            pyfalog.warning('Unable to find projected drone')
            return False
        self.savedState = drone.amountActive > 0

        if self.state == self.savedState:
            return False

        if self.state:
            if not drone.canBeApplied(fit):
                pyfalog.warning('Projected drone cannot be applied')
                return False
            drone.amountActive = drone.amount
        else:
            drone.amountActive = 0

        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of projected drone {} state to {} for fit {}'.format(self.itemID, self.state, self.fitID))
        cmd = CalcChangeProjectedDroneStateCommand(
            fitID=self.fitID,
            itemID=self.itemID,
            state=self.savedState)
        return cmd.Do()
