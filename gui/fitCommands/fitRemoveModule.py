import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .helpers import ModuleInfoCache
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveModuleCommand(wx.Command):
    """"
    Fitting command that removes a module at a specified positions

    from sFit.removeModule
    """
    def __init__(self, fitID: int, positions: list = None):
        wx.Command.__init__(self, True, "Module Remove")
        self.fitID = fitID
        self.positions = positions
        self.modCache = []
        self.change = None

    def Do(self):
        fitID = self.fitID
        pyfalog.debug("Removing module from position ({0}) for fit ID: {1}", self.positions, fitID)
        fit = eos.db.getFit(fitID)

        for x in self.positions:
            mod = fit.modules[x]
            if not mod.isEmpty:
                self.modCache.append(ModuleInfoCache(mod.modPosition, mod.item.ID, mod.state, mod.charge))
                fit.modules.toDummy(x)

        # if no modules have changes, report back None
        if not len(self.modCache) > 0:
            return False

        numSlots = len(fit.modules)
        # todo: determine if we need to do this still
        # self.recalc(fit)
        # self.checkStates(fit, None)
        fit.fill()
        eos.db.commit()
        self.slotsChanged = numSlots != len(fit.modules)
        return True

    def Undo(self):
        from .fitAddModule import FitAddModuleCommand  # avoids circular import
        for mod in self.modCache:
            cmd = FitAddModuleCommand(self.fitID, mod.itemID)
            cmd.Do()
            cmd.module.state = mod.state
            cmd.module.charge = mod.charge
        return True
