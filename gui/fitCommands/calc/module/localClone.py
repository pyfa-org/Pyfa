import copy

import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcCloneLocalModuleCommand(wx.Command):

    def __init__(self, fitID, srcPosition, dstPosition):
        wx.Command.__init__(self, True, 'Clone Local Module')
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing cloning of local module from position {} to position {} for fit ID {}'.format(self.srcPosition, self.dstPosition, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        srcMod = fit.modules[self.srcPosition]
        copyMod = copy.deepcopy(srcMod)
        if not copyMod.fits(fit):
            return False
        if not fit.modules[self.dstPosition].isEmpty:
            return False
        fit.modules.replace(self.dstPosition, copyMod)
        if copyMod not in fit.modules:
            pyfalog.warning('Failed to replace module')
            return False
        # Need to flush because checkStates sometimes relies on module->fit
        # relationship via .owner attribute, which is handled by SQLAlchemy
        eos.db.flush()
        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, copyMod)
        return True

    def Undo(self):
        pyfalog.debug('Undoing cloning of local module from position {} to position {} for fit ID {}'.format(self.srcPosition, self.dstPosition, self.fitID))
        from .localRemove import CalcRemoveLocalModulesCommand
        cmd = CalcRemoveLocalModulesCommand(fitID=self.fitID, positions=[self.dstPosition], recalc=False)
        if not cmd.Do():
            return False
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        return True

    @property
    def needsGuiRecalc(self):
        if self.savedStateCheckChanges is None:
            return True
        for container in self.savedStateCheckChanges:
            if len(container) > 0:
                return True
        return False
