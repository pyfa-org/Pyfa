import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcSwapLocalModuleCommand(wx.Command):

    def __init__(self, fitID, position1, position2):
        wx.Command.__init__(self, True, 'Swap Modules')
        self.fitID = fitID
        self.position1 = position1
        self.position2 = position2

    def Do(self):
        pyfalog.debug('Doing swapping between {} and {} for fit {}'.format(self.position1, self.position2, self.fitID))
        self.__swap(self.fitID, self.position1, self.position2)
        return True

    def Undo(self):
        self.__swap(self.fitID, self.position2, self.position1)
        pyfalog.debug('Undoing swapping between {} and {} for fit {}'.format(self.position1, self.position2, self.fitID))
        return True

    def __swap(self, fitID, srcPosition, dstPosition):
        fit = Fit.getInstance().getFit(fitID)
        srcMod = fit.modules[srcPosition]
        dstMod = fit.modules[dstPosition]
        fit.modules.free(srcPosition)
        fit.modules.free(dstPosition)
        try:
            fit.modules.replace(dstPosition, srcMod)
        except HandledListActionError:
            fit.modules.replace(srcPosition, srcMod)
            fit.modules.replace(dstPosition, dstMod)
            return False
        try:
            fit.modules.replace(srcPosition, dstMod)
        except HandledListActionError:
            fit.modules.free(dstPosition)
            fit.modules.replace(srcPosition, srcMod)
            fit.modules.replace(dstPosition, dstMod)
            return False
        eos.db.commit()
        return True
