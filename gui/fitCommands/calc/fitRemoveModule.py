import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import ModuleInfoCache


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
                self.modCache.append(ModuleInfoCache(
                    mod.modPosition,
                    mod.item.ID,
                    mod.state,
                    mod.chargeID,
                    mod.baseItemID,
                    mod.mutaplasmidID,
                    {m.attrID: m.value for m in mod.mutators.values()}))
                fit.modules.toDummy(x)

        # if no modules have changes, skip command
        if not len(self.modCache) > 0:
            return False

        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug("Reapplying {} removed module(s) for {}", len(self.modCache), self.fitID)

        from gui.fitCommands.calc.fitReplaceModule import FitReplaceModuleCommand  # avoids circular import
        for modInfo in self.modCache:
            pyfalog.debug(" -- {}", modInfo)
            cmd = FitReplaceModuleCommand(
                fitID=self.fitID,
                position=modInfo.modPosition,
                newItemID=modInfo.itemID,
                newBaseItemID=modInfo.baseID,
                newMutaplasmidID=modInfo.mutaplasmidID,
                newMutations=modInfo.mutations,
                newState=modInfo.state,
                newChargeID=modInfo.chargeID)
            cmd.Do()
        return True
