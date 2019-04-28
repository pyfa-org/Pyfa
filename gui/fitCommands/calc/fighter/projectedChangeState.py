import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFighterStateCommand(wx.Command):

    def __init__(self, fitID, position, state, commit=True):
        wx.Command.__init__(self, True, 'Change Projected Fighter State')
        self.fitID = fitID
        self.position = position
        self.state = state
        self.commit = commit
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing changing of projected fighter state to {} at position {} for fit {}'.format(
            self.state, self.position, self.fitID))

        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.projectedFighters[self.position]
        self.savedState = fighter.active

        if self.state == self.savedState:
            return False

        fighter.active = self.state

        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of projected fighter state to {} at position {} for fit {}'.format(
            self.state, self.position, self.fitID))
        cmd = CalcChangeProjectedFighterStateCommand(
            fitID=self.fitID,
            position=self.position,
            state=self.savedState,
            commit=self.commit)
        return cmd.Do()
