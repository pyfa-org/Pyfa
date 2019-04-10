import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleProjectedFitCommand(wx.Command):

    def __init__(self, fitID, projectingFitID):
        wx.Command.__init__(self, True, "Toggle Projected Fit")
        self.fitID = fitID
        self.projectingFitID = projectingFitID

    def Do(self):
        pyfalog.debug("Toggling projected fit {} for fit ID: {}".format(self.projectingFitID, self.fitID))
        projector = Fit.getInstance().getFit(self.projectingFitID)
        projectionInfo = projector.getProjectionInfo(self.fitID)
        if not projectionInfo:
            return False
        projectionInfo.active = not projectionInfo.active

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleProjectedFitCommand(self.fitID, self.projectingFitID)
        return cmd.Do()
