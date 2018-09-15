import wx
import eos.db
from logbook import Logger
import copy
pyfalog = Logger(__name__)


class FitCloneModuleCommand(wx.Command):
    """
    Clone a module from src to dst
    This will overwrite dst! Checking for empty module must be
    done at a higher level

    from sFit.cloneModule
    """
    def __init__(self, fitID, src, dst):
        wx.Command.__init__(self, True, "Module Clone")
        self.fitID = fitID
        self.src = src
        self.dst = dst

    def Do(self):
        fit = eos.db.getFit(self.fitID)
        # Gather modules
        srcMod = fit.modules[self.src]
        dstMod = fit.modules[self.dst]  # should be a placeholder module

        new = copy.deepcopy(srcMod)
        new.owner = fit
        if new.fits(fit):
            pyfalog.debug("Cloning {} from source {} to destination {} for fit ID {}", srcMod, self.src, self.dst, self.fitID)
            # insert copy if module meets hardpoint restrictions
            fit.modules.remove(dstMod)
            fit.modules.insert(self.dst, new)

            eos.db.commit()
            return True
        return False

    def Undo(self):
        from .fitRemoveModule import FitRemoveModuleCommand  # Avoid circular import
        cmd = FitRemoveModuleCommand(self.fitID, [self.dst])
        cmd.Do()
        return True
