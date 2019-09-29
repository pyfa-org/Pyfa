import wx
from logbook import Logger

from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeProjectedModuleProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, position, projectionRange):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.projectionRange = projectionRange
        self.savedProjectionRange = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing change of projected module projection range at position {} to range {} on fit {}'.format(
            self.position, self.projectionRange, self.fitID))

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        if mod.projectionRange == self.projectionRange:
            return False
        self.savedProjectionRange = mod.projectionRange
        mod.projectionRange = self.projectionRange

        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, mod)
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of projected module projection range at position {} to range {} on fit {}'.format(
            self.position, self.projectionRange, self.fitID))
        cmd = CalcChangeProjectedModuleProjectionRangeCommand(
            fitID=self.fitID,
            position=self.position,
            projectionRange=self.savedProjectionRange)
        result = cmd.Do()
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        return result

    @property
    def needsGuiRecalc(self):
        if self.savedStateCheckChanges is None:
            return True
        for container in self.savedStateCheckChanges:
            if len(container) > 0:
                return True
        return False
