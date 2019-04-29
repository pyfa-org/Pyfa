import wx
from logbook import Logger

import eos.db
from eos.const import FittingSlot
from gui.fitCommands.helpers import ModuleInfo, restoreCheckedStates, restoreRemovedDummies
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveLocalModulesCommand(wx.Command):

    def __init__(self, fitID, positions, commit=True):
        wx.Command.__init__(self, True, 'Remove Module')
        self.fitID = fitID
        self.positions = positions
        self.commit = commit
        self.savedSubInfos = None
        self.savedModInfos = None
        self.savedRemovedDummies = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing removal of local modules from positions {} on fit {}'.format(self.positions, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)

        self.savedSubInfos = {}
        self.savedModInfos = {}
        for position in self.positions:
            mod = fit.modules[position]
            if not mod.isEmpty:
                if mod.slot == FittingSlot.SUBSYSTEM:
                    self.savedSubInfos[position] = ModuleInfo.fromModule(mod)
                else:
                    self.savedModInfos[position] = ModuleInfo.fromModule(mod)
                fit.modules.free(position)

        if len(self.savedSubInfos) == 0 and len(self.savedModInfos) == 0:
            return False

        # Need to flush because checkStates sometimes relies on module->fit
        # relationship via .owner attribute, which is handled by SQLAlchemy
        eos.db.flush()
        self.savedRemovedDummies = sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, None)
        if self.commit:
            eos.db.commit()
        # If no modules were removed, report that command was not completed
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of local modules {} on fit {}'.format(self.savedModInfos, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        results = []
        from .localReplace import CalcReplaceLocalModuleCommand
        # Restore subsystems 1st
        if len(self.savedSubInfos) > 0:
            for position, modInfo in self.savedSubInfos.items():
                cmd = CalcReplaceLocalModuleCommand(
                    fitID=self.fitID, position=position, newModInfo=modInfo, commit=False, fill=False)
                results.append(cmd.Do())
            sFit.recalc(fit, fill=False)
        for position, modInfo in self.savedModInfos.items():
            cmd = CalcReplaceLocalModuleCommand(
                fitID=self.fitID, position=position, newModInfo=modInfo, commit=False, fill=False)
            results.append(cmd.Do())
        if not any(results):
            return False
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        restoreCheckedStates(fit, self.savedStateCheckChanges)
        if self.commit:
            eos.db.commit()
        return True
