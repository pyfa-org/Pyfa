import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveFighterCommand(wx.Command):
    """"
    Fitting command that removes a module at a specified positions

    from sFit.removeFighter
    """
    def __init__(self, fitID: int, position: int):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.change = None
        self.savedItemID = None
        self.savedAmount = None
        self.savedStatus = None
        self.savedAbilities = None

    def Do(self):
        fitID = self.fitID
        fit = Fit.getInstance().getFit(fitID)
        fighter = fit.fighters[self.position]
        self.savedItemID = fighter.itemID
        self.savedAmount = fighter.amount
        self.savedStatus = fighter.active
        self.savedAbilities = {fa.effectID: fa.active for fa in fighter.abilities}
        fit.fighters.remove(fighter)
        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddFighter import FitAddFighterCommand  # avoids circular import
        cmd = FitAddFighterCommand(self.fitID, self.savedItemID, self.savedStatus, self.savedAbilities)
        return cmd.Do()
