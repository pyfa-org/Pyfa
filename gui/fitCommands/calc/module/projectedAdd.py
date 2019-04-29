import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from eos.exception import HandledListActionError
from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, modInfo, position=None, commit=True):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newModInfo = modInfo
        self.newPosition = position
        self.commit = commit
        self.oldModInfo = None
        self.oldPosition = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing addition of projected module {} onto: {}'.format(self.newModInfo, self.fitID))
        newMod = self.newModInfo.toModule(fallbackState=FittingModuleState.ACTIVE)
        if newMod is None:
            return False

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        if not newMod.canHaveState(newMod.state, projectedOnto=fit):
            newMod.state = FittingModuleState.OFFLINE
        if not newMod.isValidCharge(newMod.charge):
            newMod.charge = None
        self.oldPosition, self.oldModInfo = fit.projectedModules.makeRoom(newMod)

        if self.newPosition is not None:
            try:
                fit.projectedModules.insert(self.newPosition, newMod)
            except HandledListActionError:
                if self.commit:
                    eos.db.commit()
                return False
        else:
            try:
                fit.projectedModules.append(newMod)
            except HandledListActionError:
                if self.commit:
                    eos.db.commit()
                return False
            self.newPosition = fit.projectedModules.index(newMod)

        # Need to flush because checkStates sometimes relies on module->fit
        # relationship via .owner attribute, which is handled by SQLAlchemy
        eos.db.flush()
        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, newMod)
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected module {} onto: {}'.format(self.newModInfo, self.fitID))
        if self.oldPosition is not None and self.oldModInfo is not None:
            cmd = CalcAddProjectedModuleCommand(
                fitID=self.fitID,
                modInfo=self.oldModInfo,
                position=self.oldPosition,
                commit=False)
            if not cmd.Do():
                return False
            restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
            if self.commit:
                eos.db.commit()
            return True
        from .projectedRemove import CalcRemoveProjectedModuleCommand
        cmd = CalcRemoveProjectedModuleCommand(
            fitID=self.fitID,
            position=self.newPosition,
            commit=False)
        if not cmd.Do():
            return False
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        if self.commit:
            eos.db.commit()
        return True
