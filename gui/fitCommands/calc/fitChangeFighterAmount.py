import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeFighterAmount(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Change Fighter Amount')
        self.fitID = fitID
        self.position = position
        self.amount = amount
        self.savedAmount = None
        self.removeCommand = None

    def Do(self):
        pyfalog.debug('Doing change of fighter amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.fighters[self.position]
        self.savedAmount = fighter.amount
        if self.amount > 0 or self.amount == -1:
            fighter.amount = min(self.amount, fighter.fighterSquadronMaxSize)
            eos.db.commit()
            return True
        else:
            from .fitRemoveFighter import FitRemoveFighterCommand
            self.removeCommand = FitRemoveFighterCommand(fitID=self.fitID, position=self.position)
            return self.removeCommand.Do()

    def Undo(self):
        pyfalog.debug('Undoing change of fighter amount to {} at position {} on fit {}'.format(self.amount, self.position, self.fitID))
        if self.removeCommand is not None:
            return self.removeCommand.Undo()
        cmd = FitChangeFighterAmount(self.fitID, self.position, self.savedAmount)
        return cmd.Do()
