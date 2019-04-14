import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleProjectedFighterStateCommand(wx.Command):

    def __init__(self, fitID, position, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Projected Fighter State')
        self.fitID = fitID
        self.position = position
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of projected fighter state at position {} for fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.projectedFighters[self.position]
        self.savedState = fighter.active
        fighter.active = not fighter.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of projected fighter state at position {} for fit {}'.format(self.position, self.fitID))
        cmd = FitToggleProjectedFighterStateCommand(fitID=self.fitID, position=self.position, forceState=self.savedState)
        return cmd.Do()
