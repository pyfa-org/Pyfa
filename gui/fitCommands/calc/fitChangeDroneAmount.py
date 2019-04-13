import math

import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import DroneInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeDroneAmount(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Change Drone Quantity')
        self.fitID = fitID
        self.position = position
        self.amount = amount
        self.savedDroneInfo = None
        self.removeCommand = None

    def Do(self):
        pyfalog.debug('Doing change of drone quantity to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        if self.amount > 0:
            fit = Fit.getInstance().getFit(self.fitID)
            drone = fit.drones[self.position]
            self.savedDroneInfo = DroneInfo.fromDrone(drone)
            drone.amount = self.amount
            if drone.amountActive > 0:
                difference = self.amount - self.savedDroneInfo.amount
                drone.amount = self.amount
                drone.amountActive = max(min(drone.amountActive + difference, drone.amount), 0)
            eos.db.commit()
            return True
        else:
            from .fitRemoveDrone import FitRemoveDroneCommand
            self.removeCommand = FitRemoveDroneCommand(fitID=self.fitID, position=self.position, amount=math.inf)
            return self.removeCommand.Do()

    def Undo(self):
        pyfalog.debug('Undoing change of drone quantity to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        if self.removeCommand is not None:
            return self.removeCommand.Undo()
        if self.savedDroneInfo is not None:
            fit = Fit.getInstance().getFit(self.fitID)
            drone = fit.drones[self.position]
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
            eos.db.commit()
            return True
        return False
