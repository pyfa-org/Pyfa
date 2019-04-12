import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, newModInfo, newPosition=None):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newModInfo = newModInfo
        self.newPosition = newPosition
        self.oldModInfo = None
        self.oldPosition = None

    def Do(self):
        pyfalog.debug('Doing projection of module {} onto: {}'.format(self.newModInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        newMod = self.newModInfo.toModule(fallbackState=FittingModuleState.ACTIVE)
        if newMod is None:
            return False

        if not newMod.canHaveState(newMod.state, fit):
            newMod.state = FittingModuleState.OFFLINE

        self.oldPosition, self.oldModInfo = fit.projectedModules.makeRoom(newMod)

        if self.newPosition is not None:
            fit.projectedModules.insert(self.newPosition, newMod)
            if not fit.projectedModules.lastOpState:
                self.Undo()
                return False
        else:
            fit.projectedModules.append(newMod)
            if not fit.projectedModules.lastOpState:
                self.Undo()
                return False
            self.newPosition = fit.projectedModules.index(newMod)

        eos.db.commit()
        return True

    def Undo(self):
        if self.oldPosition is not None and self.oldModInfo is not None:
            cmd = FitAddProjectedModuleCommand(
                fitID=self.fitID,
                newModInfo=self.oldModInfo,
                newPosition=self.oldPosition)
            return cmd.Do()
        from gui.fitCommands.calc.fitRemoveProjectedModule import FitRemoveProjectedModuleCommand
        cmd = FitRemoveProjectedModuleCommand(self.fitID, self.newPosition)
        cmd.Do()
        return True
