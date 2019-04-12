import wx
from logbook import Logger

import eos.db
from service.fit import Fit
from gui.fitCommands.helpers import ModuleInfo


pyfalog = Logger(__name__)


class FitRemoveProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.savedModInfo = None

    def Do(self):
        pyfalog.debug("Removing ({}) onto: {}".format(self.fitID, self.position))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        self.savedModInfo = ModuleInfo.fromModule(mod)
        del fit.projectedModules[self.position]
        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedModule import FitAddProjectedModuleCommand
        cmd = FitAddProjectedModuleCommand(
            fitID=self.fitID,
            newModInfo=self.savedModInfo,
            newPosition=self.position)
        return cmd.Do()
