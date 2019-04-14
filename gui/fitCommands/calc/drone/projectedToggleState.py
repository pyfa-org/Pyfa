import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleProjectedDroneStateCommand(wx.Command):

    def __init__(self, fitID, itemID, forceAmountActive=None):
        wx.Command.__init__(self, True, 'Toggle Projected Drone State')
        self.fitID = fitID
        self.itemID = itemID
        self.forceAmountActive = forceAmountActive
        self.savedAmountActive = None

    def Do(self):
        pyfalog.debug('Doing toggling of projected drone {} state for fit {}'.format(self.itemID, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.itemID), None)
        if drone is None:
            pyfalog.warning('Unable to find projected drone')
            return False
        self.savedAmountActive = drone.amountActive
        if self.forceAmountActive is not None:
            if self.forceAmountActive > 0 and not drone.canBeApplied(fit):
                pyfalog.warning('Projected drone cannot be applied')
                return False
            drone.amountActive = self.forceAmountActive
        elif drone.amountActive > 0:
            drone.amountActive = 0
        else:
            if not drone.canBeApplied(fit):
                pyfalog.warning('Projected drone cannot be applied')
                return False
            drone.amountActive = drone.amount
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of projected drone {} state for fit {}'.format(self.itemID, self.fitID))
        cmd = FitToggleProjectedDroneStateCommand(fitID=self.fitID, itemID=self.itemID, forceAmountActive=self.savedAmountActive)
        return cmd.Do()
