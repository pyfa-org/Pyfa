import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, modInfo, position=None, ignoreRestrictions=False, recalc=True):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newModInfo = modInfo
        self.newPosition = position
        self.ignoreRestrictions = ignoreRestrictions
        self.recalc = recalc
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
        canHaveState = newMod.canHaveState(newMod.state, projectedOnto=fit)
        if canHaveState is not True:
            newMod.state = canHaveState
        if not self.ignoreRestrictions and not newMod.isValidCharge(newMod.charge):
            newMod.charge = None
        self.oldPosition, self.oldModInfo = fit.projectedModules.makeRoom(newMod)

        if self.newPosition is not None:
            fit.projectedModules.insert(self.newPosition, newMod)
            if newMod not in fit.projectedModules:
                return False
        else:
            fit.projectedModules.append(newMod)
            if newMod not in fit.projectedModules:
                return False
            self.newPosition = fit.projectedModules.index(newMod)

        if self.recalc:
            # Need to flush because checkStates sometimes relies on module->fit
            # relationship via .owner attribute, which is handled by SQLAlchemy
            eos.db.flush()
            sFit.recalc(fit)
            self.savedStateCheckChanges = sFit.checkStates(fit, newMod)
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected module {} onto: {}'.format(self.newModInfo, self.fitID))
        if self.oldPosition is not None and self.oldModInfo is not None:
            cmd = CalcAddProjectedModuleCommand(
                fitID=self.fitID,
                modInfo=self.oldModInfo,
                position=self.oldPosition,
                ignoreRestrictions=True,
                recalc=False)
            if not cmd.Do():
                return False
            restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
            return True
        from .projectedRemove import CalcRemoveProjectedModuleCommand
        cmd = CalcRemoveProjectedModuleCommand(
            fitID=self.fitID,
            position=self.newPosition,
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
