import wx
from logbook import Logger

from gui.fitCommands.helpers import DroneInfo, droneStackLimit
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class CalcAddLocalDroneCommand(wx.Command):

    def __init__(self, fitID, droneInfo, forceNewStack=False, ignoreRestrictions=False):
        wx.Command.__init__(self, True, 'Add Local Drone')
        self.fitID = fitID
        self.droneInfo = droneInfo
        self.forceNewStack = forceNewStack
        self.ignoreRestrictions = ignoreRestrictions
        self.savedDroneInfo = None
        self.savedPosition = None

    def Do(self):
        pyfalog.debug('Doing addition of local drone {} to fit {}'.format(self.droneInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        item = Market.getInstance().getItem(self.droneInfo.itemID, eager=("attributes", "group.category"))
        # If we're not adding any active drones, check if there's an inactive stack
        # with enough space for new drones and use it
        if not self.forceNewStack and self.droneInfo.amountActive == 0:
            maxStack = droneStackLimit(fit, item)
            for drone in fit.drones.find(item):
                if (
                    drone is not None and drone.amountActive == 0 and
                    drone.amount + self.droneInfo.amount <= maxStack
                ):
                    self.savedDroneInfo = DroneInfo.fromDrone(drone)
                    self.savedPosition = fit.drones.index(drone)
                    drone.amount += self.droneInfo.amount
                    return True
        # Do new stack otherwise
        drone = self.droneInfo.toDrone()
        if drone is None:
            return False
        if not self.ignoreRestrictions and not drone.fits(fit):
            pyfalog.warning('Drone does not fit')
            return False
        fit.drones.append(drone)
        if drone not in fit.drones:
            pyfalog.warning('Failed to append to list')
            return False
        self.savedPosition = fit.drones.index(drone)
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of local drone {} to fit {}'.format(self.droneInfo, self.fitID))
        if self.savedDroneInfo is not None:
            fit = Fit.getInstance().getFit(self.fitID)
            drone = fit.drones[self.savedPosition]
            drone.amount = self.savedDroneInfo.amount
            drone.amountActive = self.savedDroneInfo.amountActive
            return True
        from .localRemove import CalcRemoveLocalDroneCommand
        cmd = CalcRemoveLocalDroneCommand(
            fitID=self.fitID,
            position=self.savedPosition,
            amount=self.droneInfo.amount)
        return cmd.Do()
