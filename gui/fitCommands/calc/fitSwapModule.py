import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitSwapModuleCommand(wx.Command):

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

    def __swap(self, fitID, src, dst):
        fit = Fit.getInstance().getFit(fitID)
        srcMod = fit.modules[src]
        dstMod = fit.modules[dst]
        fit.modules.free(src)
        fit.modules.free(dst)
        fit.modules.replace(dst, srcMod)
        fit.modules.replace(src, dstMod)
        eos.db.commit()
