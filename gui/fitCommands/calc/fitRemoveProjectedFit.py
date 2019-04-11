import wx
from logbook import Logger

import eos.db
from service.fit import Fit
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
        self.savedState = None

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}".format(self.fitID, self.projectedFitID))
        sFit = Fit.getInstance()
        projectee = sFit.getFit(self.fitID)
        projector = sFit.getFit(self.projectedFitID)

        if projector is None:
            return False

        projectionInfo = projector.getProjectionInfo(self.fitID)
        if not projectionInfo:
            return False

        self.savedState = projectionInfo.active

        del projectee.projectedFitDict[projector.ID]

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedFit import FitAddProjectedFitCommand
        cmd = FitAddProjectedFitCommand(self.fitID, self.projectedFitID, self.savedState)
        return cmd.Do()
