import wx
import eos.db
from logbook import Logger
from eos.saveddata.drone import Drone
pyfalog = Logger(__name__)


class FitAddDroneCommand(wx.Command):
    """"
    from sFit.addDrone
    """
    def __init__(self, fitID, itemID, amount=1, replace=False):
        wx.Command.__init__(self, True, "Drone add")
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount  # add x amount. If this goes over amount, removes stack
        self.replace = replace  # if this is false, we increment.
        self.index = None

    def Do(self):
        pyfalog.debug("Adding {0} drones ({1}) to fit ID: {2}", self.amount, self.itemID, self.fitID)

        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager=("attributes", "group.category"))

        for d in fit.drones.find(item):
            if d is not None and d.amountActive == 0 and d.amount < max(5, fit.extraAttributes["maxActiveDrones"]):
                drone = d
                break
        else:
            try:
                drone = Drone(item)
            except ValueError:
                pyfalog.warning("Invalid drone: {}", item)
                return False

            if not drone.fits(fit):
                return False
            fit.drones.append(drone)

        drone.amount += self.amount
        eos.db.commit()
        self.index = fit.drones.index(drone)
        return True

    def Undo(self):
        from .fitRemoveDrone import FitRemoveDroneCommand  # Avoid circular import
        cmd = FitRemoveDroneCommand(self.fitID, self.index, self.amount)
        return cmd.Do()
