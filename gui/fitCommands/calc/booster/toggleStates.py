import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleBoosterStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Booster States')
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of booster state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        positions = self.positions[:]
        if self.mainPosition not in positions:
            positions.append(self.mainPosition)
        self.savedStates = {p: fit.boosters[p].active for p in positions}

        if self.forceStates is not None:
            for position, state in self.forceStates.items():
                booster = fit.boosters[position]
                booster.active = state
        elif fit.boosters[self.mainPosition].active:
            for position in positions:
                booster = fit.boosters[position]
                if booster.active:
                    booster.active = False
        else:
            for position in positions:
                booster = fit.boosters[position]
                if not booster.active:
                    booster.active = True
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of booster state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        cmd = CalcToggleBoosterStatesCommand(
            fitID=self.fitID,
            mainPosition=self.mainPosition,
            positions=self.positions,
            forceStates=self.savedStates)
        return cmd.Do()
