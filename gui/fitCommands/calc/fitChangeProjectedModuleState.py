import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeProjectedModuleStateCommand(wx.Command):

    def __init__(self, fitID, position, click):
        wx.Command.__init__(self, True, 'Change Projected Module State')
        self.fitID = fitID
        self.position = position
        self.click = click
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing change of projected module state at position {} to click {} on fit {}'.format(self.position, self.click, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        self.savedState = mod.state
        proposedState = mod.getProposedState(mod, self.click)
        if mod.state == proposedState:
            return False
        if not mod.canHaveState(proposedState, fit):
            return False
        mod.state = proposedState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected module state at position {} to click {} on fit {}'.format(self.position, self.click, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        mod.state = self.savedState
        return True
