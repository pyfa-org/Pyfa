import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitSwapModuleCommand(wx.Command):
    """"
    from sFit.swapModules
    """
    def __init__(self, fitID, src, dst):
        wx.Command.__init__(self, True, "Module Swap")
        self.fitID = fitID
        self.src = src
        self.dst = dst

    def Do(self):
        self.__swap(self.fitID, self.src, self.dst)
        return True

    def Undo(self):
        self.__swap(self.fitID, self.dst, self.src)
        return True

    def __swap(self, fitID, src, dst):
        pyfalog.debug("Swapping modules from source ({0}) to destination ({1}) for fit ID: {1}", src, dst, fitID)
        fit = eos.db.getFit(fitID)
        # Gather modules
        srcMod = fit.modules[src]
        dstMod = fit.modules[dst]

        # To swap, we simply remove mod and insert at destination.
        fit.modules.remove(srcMod)
        fit.modules.insert(dst, srcMod)
        fit.modules.remove(dstMod)
        fit.modules.insert(src, dstMod)

        eos.db.commit()
