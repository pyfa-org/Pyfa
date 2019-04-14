import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleDroneStateCommand(wx.Command):

    def __init__(self, fitID, position, forceAmountActive=None):
        wx.Command.__init__(self, True, 'Toggle Drone State')
        self.fitID = fitID
        self.position = position
        self.forceAmountActive = forceAmountActive
        self.savedAmountActive = None

    def Do(self):
        pyfalog.debug('Doing toggling of drone state at position {} for fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        drone = fit.drones[self.position]
        self.savedAmountActive = drone.amountActive
        if self.forceAmountActive is not None:
            drone.amountActive = self.forceAmountActive
        elif drone.amountActive > 0:
            drone.amountActive = 0
        else:
            drone.amountActive = drone.amount
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of drone state at position {} for fit {}'.format(self.position, self.fitID))
        cmd = FitToggleDroneStateCommand(fitID=self.fitID, position=self.position, forceAmountActive=self.savedAmountActive)
        return cmd.Do()
