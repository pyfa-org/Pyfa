import wx
from logbook import Logger

from gui.fitCommands.helpers import DroneInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveProjectedDroneCommand(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Remove Projected Drone')
        self.fitID = fitID
        self.itemID = itemID
        self.amountToRemove = amount
        self.savedDroneInfo = None

    def Do(self):
        pyfalog.debug('Doing removal of {} projected drones {} from fit {}'.format(self.amountToRemove, self.itemID, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.itemID), None)
        if drone is None:
            pyfalog.warning('Unable to find projected drone')
            return False
        self.savedDroneInfo = DroneInfo.fromDrone(drone)
        drone.amount = max(drone.amount - self.amountToRemove, 0)
        # Remove stack if we have no items remaining
        if drone.amount == 0:
            fit.projectedDrones.remove(drone)
        else:
            if drone.amountActive > 0:
                drone.amountActive = min(drone.amountActive, drone.amount)
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of {} projected drones {} from fit {}'.format(self.amountToRemove, self.itemID, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        # Change stack if we still have it
        drone = next((pd for pd in fit.projectedDrones if pd.itemID == self.savedDroneInfo.itemID), None)
        if drone is not None:
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
            return True
        # Make new stack
        from .projectedAdd import CalcAddProjectedDroneCommand
        cmd = CalcAddProjectedDroneCommand(fitID=self.fitID, droneInfo=self.savedDroneInfo)
        return cmd.Do()
