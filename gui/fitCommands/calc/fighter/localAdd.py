import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddLocalFighterCommand(wx.Command):

    def __init__(self, fitID, fighterInfo, position=None, ignoreRestrictions=False):
        wx.Command.__init__(self, True, 'Add Fighter')
        self.fitID = fitID
        self.fighterInfo = fighterInfo
        self.position = position
        self.ignoreRestrictions = ignoreRestrictions

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
            fit.fighters.append(fighter)
            if fighter not in fit.fighters:
                pyfalog.warning('Failed to append to list')
                return False
            self.position = fit.fighters.index(fighter)
        else:
            fit.fighters.insert(self.position, fighter)
            if fighter not in fit.fighters:
                pyfalog.warning('Failed to insert to list')
                return False
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of fighter {} to fit {}'.format(self.fighterInfo, self.fitID))
        from .localRemove import CalcRemoveLocalFighterCommand
        cmd = CalcRemoveLocalFighterCommand(fitID=self.fitID, position=self.position)
        cmd.Do()
        return True
