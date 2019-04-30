import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddLocalFighterCommand(wx.Command):

    def __init__(self, fitID, fighterInfo, position=None, ignoreRestrictions=False, commit=True):
        wx.Command.__init__(self, True, 'Add Fighter')
        self.fitID = fitID
        self.fighterInfo = fighterInfo
        self.position = position
        self.ignoreRestrictions = ignoreRestrictions
        self.commit = commit

    def Do(self):
        pyfalog.debug('Doing addition of fighter {} to fit {}'.format(self.fighterInfo, self.fitID))
        fighter = self.fighterInfo.toFighter()
        if fighter is None:
            return False

        fit = Fit.getInstance().getFit(self.fitID)
        if not self.ignoreRestrictions and not fighter.fits(fit):
            pyfalog.warning('Fighter does not fit')
            return False

        # If we were not asked to set specific state, figure it out based on available tubes
        if self.fighterInfo.state is None:
            typeUsed = fit.getSlotsUsed(fighter.slot)
            typeTotal = fit.getNumSlots(fighter.slot)

            if fit.fighterTubesUsed >= fit.fighterTubesTotal or typeUsed >= typeTotal:
                fighter.active = False
            else:
                fighter.active = True

        if self.position is None:
            try:
                fit.fighters.append(fighter)
            except HandledListActionError:
                pyfalog.warning('Failed to append to list')
                if self.commit:
                    eos.db.commit()
                return False
            self.position = fit.fighters.index(fighter)
        else:
            try:
                fit.fighters.insert(self.position, fighter)
            except HandledListActionError:
                pyfalog.warning('Failed to insert to list')
                if self.commit:
                    eos.db.commit()
                return False
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of fighter {} to fit {}'.format(self.fighterInfo, self.fitID))
        from .localRemove import CalcRemoveLocalFighterCommand
        cmd = CalcRemoveLocalFighterCommand(fitID=self.fitID, position=self.position, commit=self.commit)
        cmd.Do()
        return True
