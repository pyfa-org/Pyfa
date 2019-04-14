import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleFighterStateCommand(wx.Command):

    def __init__(self, fitID, projected, position, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Fighter State')
        self.fitID = fitID
        self.projected = projected
        self.position = position
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of fighter state at position {} for fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        container = fit.projectedFighters if self.projected else fit.fighters
        fighter = container[self.position]
        self.savedState = fighter.active
        fighter.active = not fighter.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of fighter state at position {} for fit {}'.format(self.position, self.fitID))
        cmd = CalcToggleFighterStateCommand(fitID=self.fitID, projected=self.projected, position=self.position, forceState=self.savedState)
        return cmd.Do()
