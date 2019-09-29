import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedFighterProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, position, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Fighter Projection Range')
        self.fitID = fitID
        self.position = position
        self.projectionRange = projectionRange
        self.savedProjectionRange = None

    def Do(self):
        pyfalog.debug('Doing changing of projected fighter projection range to {} at position {} for fit {}'.format(
            self.projectionRange, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.projectedFighters[self.position]
        if fighter.projectionRange == self.projectionRange:
            return False
        self.savedProjectionRange = fighter.projectionRange
        fighter.projectionRange = self.projectionRange
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of projected fighter projection range to {} at position {} for fit {}'.format(
            self.projectionRange, self.position, self.fitID))
        cmd = CalcChangeProjectedFighterProjectionRangeCommand(
            fitID=self.fitID,
            position=self.position,
            projectionRange=self.savedProjectionRange)
        return cmd.Do()
