import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import ModuleInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveLocalModuleCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Module')
        self.fitID = fitID
        self.positions = positions
        self.savedModInfos = {}

    def Do(self):
        pyfalog.debug('Doing removal of local modules from positions {} on fit {}'.format(self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        for position in self.positions:
            mod = fit.modules[position]
            if not mod.isEmpty:
                self.savedModInfos[position] = ModuleInfo.fromModule(mod)
                fit.modules.free(position)

        # If no modules were removed, report that command was not completed
        if not len(self.savedModInfos) > 0:
            eos.db.commit()
            return False
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of local modules {} on fit {}'.format(self.savedModInfos, self.fitID))
        results = []
        from .localReplace import CalcReplaceLocalModuleCommand
        for position, modInfo in self.savedModInfos.items():
            cmd = CalcReplaceLocalModuleCommand(fitID=self.fitID, position=position, newModInfo=modInfo)
            results.append(cmd.Do())
        return any(results)
