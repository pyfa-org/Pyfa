import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleProjectedDroneCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Toggle Projected Drone")
        self.fitID = fitID
        self.position = position

    def Do(self):
        pyfalog.debug("Toggling projected drone for fit ID: {}".format(self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = fit.projectedDrones[self.position]

        if drone.amountActive == 0:
            if not drone.canBeApplied(fit):
                return False
            drone.amountActive = drone.amount
        else:
            drone.amountActive = 0

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleProjectedDroneCommand(self.fitID, self.position)
        return cmd.Do()
