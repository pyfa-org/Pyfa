import wx
from logbook import Logger

import eos.db
from eos.saveddata.drone import Drone
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitRemoveDroneCommand(wx.Command):
    """"
    from sFit.addDrone
    """
    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True, "Drone add")
        self.fitID = fitID
        self.position = position
        self.amountToRemove = amount
        self.savedItemID = None
        self.savedAmount = None
        self.savedAmountActive = None
        self.removedStack = None

    def Do(self):
        pyfalog.debug("Removing {0} drones for fit ID: {1}", self.amountToRemove, self.fitID)
        fit = Fit.getInstance().getFit(self.fitID)
        drone = fit.drones[self.position]
        self.savedItemID = drone.itemID
        self.savedAmount = drone.amount
        self.savedAmountActive = drone.amountActive

        drone.amount -= self.amountToRemove
        if drone.amountActive > 0:
            drone.amountActive -= self.amountToRemove

        if drone.amount == 0:
            del fit.drones[self.position]
            self.removedStack = True
        else:
            self.removedStack = False
        eos.db.commit()
        return True

    def Undo(self):
        fit = Fit.getInstance().getFit(self.fitID)
        if self.removedStack:
            droneItem = Market.getInstance().getItem(self.savedItemID, eager=("attributes", "group.category"))
            try:
                drone = Drone(droneItem)
            except ValueError:
                pyfalog.warning("Invalid drone: {}", droneItem)
                return False
            if not drone.fits(fit):
                return False
            drone.amount = self.savedAmount
            drone.amountActive = self.savedAmountActive
            fit.drones.insert(self.position, drone)
        else:
            drone = fit.drones[self.position]
            drone.amount = self.savedAmount
            drone.amountActive = self.savedAmountActive
        eos.db.commit()
        return True
