import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


# this has the same exact definition that regular rpojected modules, besides the undo
class FitRemoveProjectedFighterCommand(wx.Command):
    """"
    from sFit.project
    """

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.savedItemID = None
        self.savedAmount = None
        self.savedStatus = None
        self.savedAbilities = None

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}", self.fitID, self.position)
        fit = eos.db.getFit(self.fitID)
        fighter = fit.projectedFighters[self.position]
        self.savedItemID = fighter.itemID
        self.savedAmount = fighter.amount
        self.savedStatus = fighter.active
        self.savedAbilities = {fa.effectID: fa.active for fa in fighter.abilities}
        fit.projectedFighters.remove(fighter)
        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedFighter import FitAddProjectedFighterCommand
        cmd = FitAddProjectedFighterCommand(
            fitID=self.fitID,
            itemID=self.savedItemID,
            state=self.savedStatus,
            abilities=self.savedAbilities)
        cmd.Do()
        return True
