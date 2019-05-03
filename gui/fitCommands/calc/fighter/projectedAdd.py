import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddProjectedFighterCommand(wx.Command):

    def __init__(self, fitID, fighterInfo, position=None, commit=True):
        wx.Command.__init__(self, True, 'Add Projected Fighter')
        self.fitID = fitID
        self.fighterInfo = fighterInfo
        self.position = position
        self.commit = commit

    def Do(self):
        pyfalog.debug('Doing addition of projected fighter {} onto: {}'.format(self.fighterInfo, self.fitID))
        fighter = self.fighterInfo.toFighter()
        if fighter is None:
            return False
        fit = Fit.getInstance().getFit(self.fitID)
        if self.position is not None:
            fit.projectedFighters.insert(self.position, fighter)
            if fighter not in fit.projectedFighters:
                if self.commit:
                    eos.db.commit()
                return False
        else:
            fit.projectedFighters.append(fighter)
            if fighter not in fit.projectedFighters:
                if self.commit:
                    eos.db.commit()
                return False
            self.position = fit.projectedFighters.index(fighter)
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected fighter {} onto: {}'.format(self.fighterInfo, self.fitID))
        from .projectedRemove import CalcRemoveProjectedFighterCommand
        cmd = CalcRemoveProjectedFighterCommand(fitID=self.fitID, position=self.position, commit=self.commit)
        return cmd.Do()
