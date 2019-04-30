import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from gui.fitCommands.helpers import ModuleInfo, restoreCheckedStates, stateLimit
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcReplaceLocalModuleCommand(wx.Command):

    def __init__(self, fitID, position, newModInfo, unloadInvalidCharges=False, commit=True):
        wx.Command.__init__(self, True, 'Replace Module')
        self.fitID = fitID
        self.position = position
        self.newModInfo = newModInfo
        self.oldModInfo = None
        self.unloadInvalidCharges = unloadInvalidCharges
        self.commit = commit
        self.savedStateCheckChanges = None
        self.unloadedCharge = None

    def Do(self):
        pyfalog.debug('Doing replacement of local module at position {} to {} on fit {}'.format(self.position, self.newModInfo, self.fitID))
        self.unloadedCharge = False
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldMod = fit.modules[self.position]
        if not oldMod.isEmpty:
            self.oldModInfo = ModuleInfo.fromModule(oldMod)
        if self.newModInfo == self.oldModInfo:
            return False
        newMod = self.newModInfo.toModule(fallbackState=stateLimit(self.newModInfo.itemID))
        if newMod is None:
            return False
        if newMod.slot != oldMod.slot:
            return False
        # Dummy it out in case the next bit fails
        fit.modules.free(self.position)
        if not newMod.fits(fit):
            pyfalog.warning('Module does not fit')
            self.Undo()
            return False
        if not newMod.isValidCharge(newMod.charge):
            if self.unloadInvalidCharges:
                newMod.charge = None
                self.unloadedCharge = True
            else:
                pyfalog.warning('Invalid charge')
                self.Undo()
                return False
        try:
            fit.modules.replace(self.position, newMod)
        except HandledListActionError:
            pyfalog.warning('Failed to replace in list')
            self.Undo()
            return False
        # Need to flush because checkStates sometimes relies on module->fit
        # relationship via .owner attribute, which is handled by SQLAlchemy
        eos.db.flush()
        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, newMod)
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing replacement of local module at position {} to {} on fit {}'.format(self.position, self.newModInfo, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        # Remove if there was no module
        if self.oldModInfo is None:
            from .localRemove import CalcRemoveLocalModulesCommand
            cmd = CalcRemoveLocalModulesCommand(fitID=self.fitID, positions=[self.position], commit=False)
            if not cmd.Do():
                return False
            restoreCheckedStates(fit, self.savedStateCheckChanges)
            if self.commit:
                eos.db.commit()
            return True
        # Replace if there was
        oldMod = self.oldModInfo.toModule()
        if oldMod is None:
            return False
        fit.modules.free(self.position)
        if not oldMod.fits(fit):
            pyfalog.warning('Module does not fit')
            self.Do()
            return False
        try:
            fit.modules.replace(self.position, oldMod)
        except HandledListActionError:
            pyfalog.warning('Failed to replace in list')
            self.Do()
            return False
        restoreCheckedStates(fit, self.savedStateCheckChanges)
        if self.commit:
            eos.db.commit()
        return True
