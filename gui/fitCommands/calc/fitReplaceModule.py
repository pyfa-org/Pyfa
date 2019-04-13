import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from gui.fitCommands.helpers import ModuleInfo, stateLimit
from service.fit import Fit


pyfalog = Logger(__name__)


class FitReplaceModuleCommand(wx.Command):

    def __init__(self, fitID, position, newModInfo):
        wx.Command.__init__(self, True, 'Replace Module')
        self.fitID = fitID
        self.position = position
        self.newModInfo = newModInfo
        self.oldModInfo = None

    def Do(self):
        pyfalog.debug('Doing replacement of module at position {} to {} on fit {}'.format(self.newModInfo, self.position, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldMod = fit.modules[self.position]
        if not oldMod.isEmpty:
            self.oldModInfo = ModuleInfo.fromModule(oldMod)
        newMod = self.newModInfo.toModule(fallbackState=stateLimit(self.newModInfo.itemID))
        if newMod is None:
            return False
        # Dummy it out in case the next bit fails
        fit.modules.free(self.position)
        if not newMod.fits(fit):
            pyfalog.warning('Module does not fit')
            self.Undo()
            return False
        newMod.owner = fit
        try:
            fit.modules.replace(self.position, newMod)
        except HandledListActionError:
            pyfalog.warning('Failed to replace in list')
            self.Undo()
            return False
        sFit.checkStates(fit, newMod)
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing replacement of module at position {} to {} on fit {}'.format(self.newModInfo, self.position, self.fitID))
        # Remove if there was no module
        if self.oldModInfo is None:
            from gui.fitCommands.calc.fitRemoveModule import FitRemoveModuleCommand
            cmd = FitRemoveModuleCommand(fitID=self.fitID, positions=[self.position])
            return cmd.Do()
        # Replace if there was
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldMod = self.oldModInfo.toModule()
        if oldMod is None:
            return False
        fit.modules.free(self.position)
        if not oldMod.fits(fit):
            pyfalog.warning('Module does not fit')
            self.Do()
            return False
        oldMod.owner = fit
        try:
            fit.modules.replace(self.position, oldMod)
        except HandledListActionError:
            pyfalog.warning('Failed to replace in list')
            self.Do()
            return False
        sFit.checkStates(fit, oldMod)
        eos.db.commit()
        return True
