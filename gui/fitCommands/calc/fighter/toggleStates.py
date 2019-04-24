import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleFighterStatesCommand(wx.Command):

    def __init__(self, fitID, projected, mainPosition, positions, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Fighter States')
        self.fitID = fitID
        self.projected = projected
        self.mainPosition = mainPosition
        self.positions = positions
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of fighter state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        container = fit.projectedFighters if self.projected else fit.fighters

        positions = self.positions[:]
        if self.mainPosition not in positions:
            positions.append(self.mainPosition)
        self.savedStates = {p: container[p].active for p in positions}

        if self.forceStates is not None:
            for position, active in self.forceStates.items():
                fighter = container[position]
                fighter.active = active
        elif container[self.mainPosition].active:
            for position in positions:
                fighter = container[position]
                if fighter.active:
                    fighter.active = False
        else:
            for position in positions:
                fighter = container[position]
                if not fighter.active:
                    fighter.active = True
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of fighter state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        cmd = CalcToggleFighterStatesCommand(
            fitID=self.fitID,
            projected=self.projected,
            mainPosition=self.mainPosition,
            positions=self.positions,
            forceStates=self.savedStates)
        return cmd.Do()
