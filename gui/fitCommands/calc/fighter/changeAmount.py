import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeFighterAmountCommand(wx.Command):

    def __init__(self, fitID, projected, position, amount):
        wx.Command.__init__(self, True, 'Change Fighter Amount')
        self.fitID = fitID
        self.projected = projected
        self.position = position
        self.amount = amount
        self.savedAmount = None

    def Do(self):
        pyfalog.debug('Doing change of fighter amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        container = fit.projectedFighters if self.projected else fit.fighters
        fighter = container[self.position]
        if self.amount == fighter.amount:
            return False
        self.savedAmount = fighter.amount
        if self.amount == -1:
            fighter.amount = self.amount
            return True
        else:
            fighter.amount = max(min(self.amount, fighter.fighterSquadronMaxSize), 0)
            return True

    def Undo(self):
        pyfalog.debug('Undoing change of fighter amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        cmd = CalcChangeFighterAmountCommand(fitID=self.fitID, projected=self.projected, position=self.position, amount=self.savedAmount)
        return cmd.Do()
