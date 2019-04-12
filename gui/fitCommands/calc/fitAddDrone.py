import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitAddDroneCommand(wx.Command):

    def __init__(self, fitID, droneInfo):
        wx.Command.__init__(self, True, 'Add Drone')
        self.fitID = fitID
        self.droneInfo = droneInfo
        self.position = None

    def Do(self):
        pyfalog.debug('Doing addition of drone {} to fit {}'.format(self.droneInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        item = Market.getInstance().getItem(self.droneInfo.itemID, eager=("attributes", "group.category"))
        # If we're not adding any active drones, check if there's an inactive stack
        # with enough space for new drones and use it
        if self.droneInfo.amountActive == 0:
            for d in fit.drones.find(item):
                if (
                    d is not None and d.amountActive == 0 and
                    d.amount + self.droneInfo.amount) <= max(5, fit.extraAttributes["maxActiveDrones"]
                ):
                    drone = d
                    drone.amount += self.droneInfo.amount
                    eos.db.commit()
                    self.position = fit.drones.index(drone)
                    return True
        # Do new stack otherwise
        drone = self.droneInfo.toDrone()
        if drone is None:
            return False
        if not drone.fits(fit):
            pyfalog.warning('Drone does not fit')
            return False
        try:
            fit.drones.append(drone)
        except HandledListActionError:
            pyfalog.warning('Failed to append to list')
            eos.db.commit()
            return False
        eos.db.commit()
        self.position = fit.drones.index(drone)
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of drone {} to fit {}'.format(self.droneInfo, self.fitID))
        from .fitRemoveDrone import FitRemoveDroneCommand
        cmd = FitRemoveDroneCommand(fitID=self.fitID, position=self.position, amount=self.droneInfo.amount)
        return cmd.Do()
