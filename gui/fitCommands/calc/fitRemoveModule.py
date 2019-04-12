import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import ModuleInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveModuleCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Module')
        self.fitID = fitID
        self.positions = positions
        self.oldModInfos = {}

    def Do(self):
        pyfalog.debug('Doing removal of modules from positions {} on fit {}'.format(self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        for position in self.positions:
            mod = fit.modules[position]
            if not mod.isEmpty:
                self.oldModInfos[position] = ModuleInfo.fromModule(mod)
                fit.modules.toDummy(position)

        # If no modules were removed, report that command was not completed
        if not len(self.oldModInfos) > 0:
            return False
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of modules {} on fit {}'.format(self.oldModInfos, self.fitID))
        from gui.fitCommands.calc.fitReplaceModule import FitReplaceModuleCommand
        for position, modInfo in self.oldModInfos.items():
            cmd = FitReplaceModuleCommand(fitID=self.fitID, position=position, newModInfo=modInfo)
            cmd.Do()
        return True
