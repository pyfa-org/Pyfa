import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFighterStateCommand(wx.Command):

    def __init__(self, fitID, position, state):
        wx.Command.__init__(self, True, 'Change Projected Fighter State')
        self.fitID = fitID
        self.position = position
        self.state = state
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

        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of projected fighter state to {} at position {} for fit {}'.format(
            self.state, self.position, self.fitID))
        cmd = CalcChangeProjectedFighterStateCommand(
            fitID=self.fitID,
            position=self.position,
            state=self.savedState)
        return cmd.Do()
