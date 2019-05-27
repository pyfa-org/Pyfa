import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleLocalFighterStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Local Fighter States')
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of local fighter state at position {}/{} for fit {}'.format(
            self.mainPosition, self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        positions = self.positions[:]
        if self.mainPosition not in positions:
            positions.append(self.mainPosition)
        self.savedStates = {p: fit.fighters[p].active for p in positions}

        if self.forceStates is not None:
            for position, state in self.forceStates.items():
                fighter = fit.fighters[position]
                fighter.active = state
        elif fit.fighters[self.mainPosition].active:
            for position in positions:
                fighter = fit.fighters[position]
                if fighter.active:
                    fighter.active = False
        else:
            for position in positions:
                fighter = fit.fighters[position]
                if not fighter.active:
                    fighter.active = True
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of local fighter state at position {}/{} for fit {}'.format(
            self.mainPosition, self.positions, self.fitID))
        cmd = CalcToggleLocalFighterStatesCommand(
            fitID=self.fitID,
            mainPosition=self.mainPosition,
            positions=self.positions,
            forceStates=self.savedStates)
        return cmd.Do()
