import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleImplantStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Implant States')
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of implant state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        positions = self.positions[:]
        if self.mainPosition not in positions:
            positions.append(self.mainPosition)
        self.savedStates = {p: fit.implants[p].active for p in positions}

        if self.forceStates is not None:
            for position, active in self.forceStates.items():
                implant = fit.implants[position]
                implant.active = active
        elif fit.implants[self.mainPosition].active:
            for position in positions:
                implant = fit.implants[position]
                if implant.active:
                    implant.active = False
        else:
            for position in positions:
                implant = fit.implants[position]
                if not implant.active:
                    implant.active = True
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of implant state at position {}/{} for fit {}'.format(self.mainPosition, self.positions, self.fitID))
        cmd = CalcToggleImplantStatesCommand(
            fitID=self.fitID,
            positions=self.positions,
            mainPosition=self.mainPosition,
            forceStates=self.savedStates)
        return cmd.Do()
