import wx
import eos.db
from logbook import Logger
from .fitRemoveProjectedModule import FitRemoveProjectedModuleCommand
pyfalog = Logger(__name__)


# this has the same exact definition that regular rpojected modules, besides the undo
class FitRemoveProjectedFitCommand(FitRemoveProjectedModuleCommand):
    """"
    from sFit.project
    """

    def __init__(self, fitID, projectedFitID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.projectedFitID = projectedFitID

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}", self.fitID, self.projectedFitID)
        fit = eos.db.getFit(self.fitID)
        projectedFit = eos.db.getFit(self.projectedFitID)

        if projectedFit is None:
            return False

        del fit.projectedFitDict[projectedFit.ID]

        eos.db.commit()
        return True

    def Undo(self):
        # todo: figure out if I need to return false here if the fit doesn't return true (means it was deleted)
        from gui.fitCommands.calc.fitAddProjectedFit import FitAddProjectedFitCommand
        cmd = FitAddProjectedFitCommand(self.fitID, self.projectedFitID)
        cmd.Do()
        return True
