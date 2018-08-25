import wx

from gui.fitCommands.helpers import ModuleInfoCache
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveModuleCommand(wx.Command):
    """"
    Fitting command that removes a module at a specified positions

    from sFit.removeModule
    """
    def __init__(self, fitID: int, positions: list = None):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.positions = positions
        self.modCache = []
        self.change = None

    def Do(self):
        fitID = self.fitID
        fit = eos.db.getFit(fitID)

        pyfalog.debug("Removing module from position ({0}) for fit ID: {1}", self.positions, fitID)

        for x in self.positions:
            mod = fit.modules[x]
            if not mod.isEmpty:
                pyfalog.debug(" -- Removing {}", mod)
                self.modCache.append(ModuleInfoCache(mod.modPosition, mod.item.ID, mod.state, mod.charge, mod.baseItemID, mod.mutaplasmidID))
                fit.modules.toDummy(x)

        # if no modules have changes, skip command
        if not len(self.modCache) > 0:
            return False

        numSlots = len(fit.modules)
        # todo: determine if we need to do this still
        # self.recalc(fit)
        # self.checkStates(fit, None)
        # fit.fill()
        eos.db.commit()
        self.slotsChanged = numSlots != len(fit.modules)
        return True

    def Undo(self):
        pyfalog.debug("Reapplying {} removed module(s) for {}", len(self.modCache), self.fitID)

        from gui.fitCommands.calc.fitReplaceModule import FitReplaceModuleCommand  # avoids circular import
        for mod in self.modCache:
            pyfalog.debug(" -- {}", mod)
            # todo, send the state and charge?
            cmd = FitReplaceModuleCommand(self.fitID, mod.modPosition, mod.itemID)
            cmd.Do()
            cmd.module.state = mod.state
            cmd.module.charge = mod.charge
        return True
