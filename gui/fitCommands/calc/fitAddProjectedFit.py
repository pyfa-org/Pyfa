import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitAddProjectedFitCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, projectedFitID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.projectedFitID = projectedFitID
        self.new_index = None
        self.old_item = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.projectedFitID)
        fit = eos.db.getFit(self.fitID)
        projectedFit = eos.db.getFit(self.projectedFitID)

        if projectedFit is None or projectedFit in fit.projectedFits:
            return False

        fit.projectedFitDict[projectedFit.ID] = projectedFit

        # this bit is required -- see GH issue # 83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(projectedFit)

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedFit import FitRemoveProjectedFitCommand  # avoids circular import
        cmd = FitRemoveProjectedFitCommand(self.fitID, self.projectedFitID)
        cmd.Do()
        return True
