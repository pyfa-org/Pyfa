import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from gui.fitCommands.helpers import DroneInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveLocalDroneCommand(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Remove Drone')
        self.fitID = fitID
        self.position = position
        self.amountToRemove = amount
        self.savedDroneInfo = None
        self.removedStack = None

    def Do(self):
        pyfalog.debug('Doing removal of {} local drones at position {} from fit {}'.format(self.amountToRemove, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = fit.drones[self.position]
        self.savedDroneInfo = DroneInfo.fromDrone(drone)

        drone.amount = max(drone.amount - self.amountToRemove, 0)
        if drone.amountActive > 0:
            drone.amountActive = min(drone.amountActive, drone.amount)

        if drone.amount == 0:
            fit.drones.remove(drone)
            self.removedStack = True
        else:
            self.removedStack = False

        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of {} local drones at position {} from fit {}'.format(self.amountToRemove, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        if self.removedStack:
            drone = self.savedDroneInfo.toDrone()
            if drone is None:
                return False
            if not drone.fits(fit):
                return False
            try:
                fit.drones.insert(self.position, drone)
            except HandledListActionError:
                pyfalog.warning('Failed to insert to list')
                eos.db.commit()
                return False
        else:
            drone = fit.drones[self.position]
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
        eos.db.commit()
        return True
