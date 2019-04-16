import math

import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import DroneInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeLocalDroneAmountCommand(wx.Command):

    def __init__(self, fitID, position, amount, commit=True):
        wx.Command.__init__(self, True, 'Change Drone Amount')
        self.fitID = fitID
        self.position = position
        self.amount = amount
        self.commit = commit
        self.savedDroneInfo = None

    def Do(self):
        pyfalog.debug('Doing change of local drone amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = fit.drones[self.position]
        self.savedDroneInfo = DroneInfo.fromDrone(drone)
        if self.amount == self.savedDroneInfo.amount:
            return False
        drone.amount = self.amount
        if drone.amountActive > 0:
            difference = self.amount - self.savedDroneInfo.amount
            drone.amount = self.amount
            drone.amountActive = max(min(drone.amountActive + difference, drone.amount), 0)
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of local drone quantity to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        if self.savedDroneInfo is not None:
            fit = Fit.getInstance().getFit(self.fitID)
            drone = fit.drones[self.position]
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
            if self.commit:
                eos.db.commit()
            return True
        return False
