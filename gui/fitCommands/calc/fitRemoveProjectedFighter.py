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
        self.removed_item = None

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}", self.fitID, self.position)
        fit = eos.db.getFit(self.fitID)

        fighter = fit.projectedFighters[self.position]
        fit.projectedFighters.remove(fighter)
        self.removed_item = fighter.itemID

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedFighter import FitAddProjectedFighterCommand
        cmd = FitAddProjectedFighterCommand(self.fitID, self.removed_item)
        cmd.Do()
        return True
