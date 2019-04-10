import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, position, click):
        wx.Command.__init__(self, True, "Toggle Projected Module")
        self.fitID = fitID
        self.position = position
        self.click = click
        self.oldState = None

    def Do(self):
        pyfalog.debug("Toggling projected module for fit ID: {}".format(self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        self.oldState = mod.state

        proposedState = mod.getProposedState(mod, self.click)
        if mod.state == proposedState:
            return False
        if not mod.canHaveState(proposedState, fit):
            return False

        mod.state = proposedState
        eos.db.commit()

        return True

    def Undo(self):
        pyfalog.debug("Toggling projected module for fit ID: {}".format(self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        mod.state = self.oldState
        return True
