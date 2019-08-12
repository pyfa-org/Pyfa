import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import ModuleInfo, restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, position, recalc=True):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.recalc = recalc
        self.savedModInfo = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing removal of projected module from position {} on fit {}'.format(self.position, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        self.savedModInfo = ModuleInfo.fromModule(mod)
        del fit.projectedModules[self.position]

        if self.recalc:
            # Need to flush because checkStates sometimes relies on module->fit
            # relationship via .owner attribute, which is handled by SQLAlchemy
            eos.db.flush()
            sFit.recalc(fit)
            self.savedStateCheckChanges = sFit.checkStates(fit, None)
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of projected module {} on fit {}'.format(self.savedModInfo, self.fitID))
        from .projectedAdd import CalcAddProjectedModuleCommand
        cmd = CalcAddProjectedModuleCommand(
            fitID=self.fitID,
            modInfo=self.savedModInfo,
            position=self.position,
            ignoreRestrictions=True,
            recalc=False)
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
