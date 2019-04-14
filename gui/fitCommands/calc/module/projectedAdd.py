import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddProjectedModuleCommand(wx.Command):

    def __init__(self, fitID, modInfo, position=None):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newModInfo = modInfo
        self.newPosition = position
        self.oldModInfo = None
        self.oldPosition = None

    def Do(self):
        pyfalog.debug('Doing addition of projected module {} onto: {}'.format(self.newModInfo, self.fitID))
        newMod = self.newModInfo.toModule(fallbackState=FittingModuleState.ACTIVE)
        if newMod is None:
            return False

        fit = Fit.getInstance().getFit(self.fitID)
        if not newMod.canHaveState(newMod.state, projectedOnto=fit):
            newMod.state = FittingModuleState.OFFLINE

        self.oldPosition, self.oldModInfo = fit.projectedModules.makeRoom(newMod)

        if self.newPosition is not None:
            try:
                fit.projectedModules.insert(self.newPosition, newMod)
            except HandledListActionError:
                eos.db.commit()
                return False
        else:
            try:
                fit.projectedModules.append(newMod)
            except HandledListActionError:
                eos.db.commit()
                return False
            self.newPosition = fit.projectedModules.index(newMod)

        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of projected module {} onto: {}'.format(self.newModInfo, self.fitID))
        if self.oldPosition is not None and self.oldModInfo is not None:
            cmd = FitAddProjectedModuleCommand(fitID=self.fitID, modInfo=self.oldModInfo, position=self.oldPosition)
            return cmd.Do()
        from .projectedRemove import FitRemoveProjectedModuleCommand
        cmd = FitRemoveProjectedModuleCommand(self.fitID, self.newPosition)
        return cmd.Do()
