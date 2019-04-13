import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from gui.fitCommands.helpers import DroneInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddProjectedDroneCommand(wx.Command):

    def __init__(self, fitID, droneInfo):
        wx.Command.__init__(self, True, 'Add Projected Drone')
        self.fitID = fitID
        self.droneInfo = droneInfo
        self.savedDroneInfo = None

    def Do(self):
        pyfalog.debug('Doing addition of projected drone {} to fit {}'.format(self.droneInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.droneInfo.itemID), None)
        # Changing existing stack
        if drone is not None:
            self.savedDroneInfo = DroneInfo.fromDrone(drone)
            # Ignore drone info's active amount parameter if we're adding to existing stack,
            # and decide based on stack's state
            drone.amount += self.droneInfo.amount
            if drone.amountActive > 0:
                drone.amountActive += self.droneInfo.amount
            eos.db.commit()
            return True
        # Making new stack
        drone = self.droneInfo.toDrone()
        if drone is None:
            return False
        if not drone.item.isType('projected'):
            pyfalog.debug('Drone is not projectable')
            return False
        try:
            fit.projectedDrones.append(drone)
        except HandledListActionError:
            pyfalog.warning('Failed to append to list')
            eos.db.commit()
            return False
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected drone {} to fit {}'.format(self.droneInfo, self.fitID))
        # Changing existing stack
        if self.savedDroneInfo is not None:
            fit = Fit.getInstance().getFit(self.fitID)
            drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.savedDroneInfo.itemID), None)
            if drone is None:
                pyfalog.warning('Unable to find projected drone for modification')
                return False
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
            return True
        # Removing new stack
        from .fitRemoveProjectedDrone import FitRemoveProjectedDroneCommand
        cmd = FitRemoveProjectedDroneCommand(self.fitID, self.droneInfo)
        return cmd.Do()
