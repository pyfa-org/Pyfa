import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleBoosterStateCommand(wx.Command):

    def __init__(self, fitID, position, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Booster State')
        self.fitID = fitID
        self.position = position
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of booster state at position {} for fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        booster = fit.boosters[self.position]
        self.savedState = booster.active
        booster.active = not booster.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of booster state at position {} for fit {}'.format(self.position, self.fitID))
        cmd = CalcToggleBoosterStateCommand(fitID=self.fitID, position=self.position, forceState=self.savedState)
        return cmd.Do()
