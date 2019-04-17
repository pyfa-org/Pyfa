import copy

import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcCloneLocalModuleCommand(wx.Command):

    def __init__(self, fitID, srcPosition, dstPosition):
        wx.Command.__init__(self, True, 'Clone Module')
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing cloning of local module from position {} to position {} for fit ID {}'.format(self.srcPosition, self.dstPosition, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        srcMod = fit.modules[self.srcPosition]
        copyMod = copy.deepcopy(srcMod)
        if not copyMod.fits(fit):
            return False
        if not fit.modules[self.dstPosition].isEmpty:
            return False
        try:
            fit.modules.replace(self.dstPosition, copyMod)
        except HandledListActionError:
            pyfalog.warning('Failed to replace module')
            eos.db.commit()
            return False
        sFit.recalc(fit)
        self.savedStateCheckChanges = sFit.checkStates(fit, copyMod)
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing cloning of local module from position {} to position {} for fit ID {}'.format(self.srcPosition, self.dstPosition, self.fitID))
        from .localRemove import CalcRemoveLocalModuleCommand
        cmd = CalcRemoveLocalModuleCommand(fitID=self.fitID, positions=[self.dstPosition])
        if not cmd.Do():
            return False
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        return True
