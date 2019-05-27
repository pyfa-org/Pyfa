import wx
from logbook import Logger

from gui.fitCommands.helpers import DroneInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedDroneAmountCommand(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Change Projected Drone Amount')
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount
        self.savedDroneInfo = None

    def Do(self):
        pyfalog.debug('Doing change of projected drone {} amount to {} on fit {}'.format(self.itemID, self.amount, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.itemID), None)
        if drone is None:
            pyfalog.warning('Cannot find projected drone')
            return False
        self.savedDroneInfo = DroneInfo.fromDrone(drone)
        if self.amount == self.savedDroneInfo.amount:
            return False
        drone.amount = self.amount
        if drone.amountActive > 0:
            difference = self.amount - self.savedDroneInfo.amount
            drone.amount = self.amount
            drone.amountActive = max(min(drone.amountActive + difference, drone.amount), 0)
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected drone {} amount to {} on fit {}'.format(self.itemID, self.amount, self.fitID))
        if self.savedDroneInfo is not None:
            fit = Fit.getInstance().getFit(self.fitID)
            drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.savedDroneInfo.itemID), None)
            if drone is None:
                pyfalog.warning('Cannot find projected drone')
                return False
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
            return True
        return False
