import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddProjectedFitCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, projectedFitID, status):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.status = status

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.projectedFitID)
        sFit = Fit.getInstance()
        projectee = sFit.getFit(self.fitID)
        projector = sFit.getFit(self.projectedFitID)

        if projector is None or projector in projectee.projectedFits:
            return False

        projectee.projectedFitDict[projector.ID] = projector

        # this bit is required -- see GH issue # 83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(projector)

        if self.status is not None:
            projectionInfo = projector.getProjectionInfo(self.fitID)
            if not projectionInfo:
                return False
            projectionInfo.active = self.status

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedFit import FitRemoveProjectedFitCommand  # avoids circular import
        cmd = FitRemoveProjectedFitCommand(self.fitID, self.projectedFitID)
        cmd.Do()
        return True
