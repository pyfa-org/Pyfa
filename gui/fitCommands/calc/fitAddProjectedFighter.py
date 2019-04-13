import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddProjectedFighterCommand(wx.Command):

    def __init__(self, fitID, fighterInfo, position=None):
        wx.Command.__init__(self, True, 'Add Projected Fighter')
        self.fitID = fitID
        self.fighterInfo = fighterInfo
        self.position = position

    def Do(self):
        pyfalog.debug('Doing addition of projected fighter {} onto: {}'.format(self.fighterInfo, self.fitID))
        fighter = self.fighterInfo.toFighter()
        if fighter is None:
            return False
        fit = Fit.getInstance().getFit(self.fitID)
        if self.position is not None:
            try:
                fit.projectedFighters.insert(self.position, fighter)
            except HandledListActionError:
                eos.db.commit()
                return False
        else:
            try:
                fit.projectedFighters.append(fighter)
            except HandledListActionError:
                eos.db.commit()
                return False
            self.position = fit.projectedFighters.index(fighter)
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected fighter {} onto: {}'.format(self.fighterInfo, self.fitID))
        from .fitRemoveProjectedFighter import FitRemoveProjectedFighterCommand
        cmd = FitRemoveProjectedFighterCommand(fitID=self.fitID, position=self.position)
        return cmd.Do()
