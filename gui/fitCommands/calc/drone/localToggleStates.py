import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleLocalDroneStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions, forceActiveAmounts=None):
        wx.Command.__init__(self, True, 'Toggle Local Drone States')
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions
        self.forceActiveAmounts = forceActiveAmounts
        self.savedActiveAmounts = None

    def Do(self):
        pyfalog.debug('Doing toggling of local drone state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        positions = self.positions[:]
        if self.mainPosition not in positions:
            positions.append(self.mainPosition)
        self.savedActiveAmounts = {p: fit.drones[p].amountActive for p in positions}

        if self.forceActiveAmounts is not None:
            for position, amountActive in self.forceActiveAmounts.items():
                drone = fit.drones[position]
                drone.amountActive = amountActive
        elif fit.drones[self.mainPosition].amountActive > 0:
            for position in positions:
                drone = fit.drones[position]
                if drone.amountActive > 0:
                    drone.amountActive = 0
        else:
            for position in positions:
                drone = fit.drones[position]
                if drone.amountActive == 0:
                    drone.amountActive = drone.amount

        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of local drone state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        cmd = CalcToggleLocalDroneStatesCommand(
            fitID=self.fitID,
            mainPosition=self.mainPosition,
            positions=self.positions,
            forceActiveAmounts=self.savedActiveAmounts)
        return cmd.Do()
