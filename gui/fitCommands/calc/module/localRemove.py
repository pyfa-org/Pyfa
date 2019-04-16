import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import ModuleInfo, restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveLocalModuleCommand(wx.Command):

    def __init__(self, fitID, positions, commit=True):
        wx.Command.__init__(self, True, 'Remove Module')
        self.fitID = fitID
        self.positions = positions
        self.savedModInfos = {}
        self.commit = commit
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing removal of local modules from positions {} on fit {}'.format(self.positions, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)

        for position in self.positions:
            mod = fit.modules[position]
            if not mod.isEmpty:
                self.savedModInfos[position] = ModuleInfo.fromModule(mod)
                fit.modules.free(position)

        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, None)
        if self.commit:
            eos.db.commit()
        # If no modules were removed, report that command was not completed
        return len(self.savedModInfos) > 0

    def Undo(self):
        pyfalog.debug('Undoing removal of local modules {} on fit {}'.format(self.savedModInfos, self.fitID))
        results = []
        from .localReplace import CalcReplaceLocalModuleCommand
        for position, modInfo in self.savedModInfos.items():
            cmd = CalcReplaceLocalModuleCommand(fitID=self.fitID, position=position, newModInfo=modInfo, commit=False)
            results.append(cmd.Do())
        if not any(results):
            return False
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        if self.commit:
            eos.db.commit()
        return True
