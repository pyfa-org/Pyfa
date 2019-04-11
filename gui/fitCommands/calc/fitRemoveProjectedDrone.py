import wx
from logbook import Logger

import eos.db
from eos.saveddata.drone import Drone
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitRemoveProjectedDroneCommand(wx.Command):
    """"
    from sFit.project
    """

    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.amountToRemove = amount
        self.savedItemID = None
        self.savedAmount = None
        self.savedAmountActive = None
        self.removedStack = None

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}".format(self.fitID, self.position))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = fit.projectedDrones[self.position]
        self.savedItemID = drone.itemID
        self.savedAmount = drone.amount
        self.savedAmountActive = drone.amountActive

        drone.amount -= self.amountToRemove
        if drone.amountActive > 0:
            drone.amountActive -= self.amountToRemove

        if drone.amount == 0:
            del fit.projectedDrones[self.position]
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
            fit.projectedDrones.insert(self.position, drone)
        else:
            drone = fit.projectedDrones[self.position]
            drone.amount = self.savedAmount
            drone.amountActive = self.savedAmountActive
        eos.db.commit()
        return True
