import wx
from logbook import Logger

import eos.db
from service.fit import Fit
from gui.fitCommands.helpers import ModuleInfoCache


pyfalog = Logger(__name__)


class FitRemoveProjectedModuleCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.savedModInfo = None

    def Do(self):
        pyfalog.debug("Removing ({}) onto: {}".format(self.fitID, self.position))
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.projectedModules[self.position]
        self.savedModInfo = ModuleInfoCache(
            modPosition=self.position,
            itemID=mod.itemID,
            state=mod.state,
            chargeID=mod.chargeID,
            baseID=None,
            mutaplasmidID=None,
            mutations={})

        del fit.projectedModules[self.position]

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedModule import FitAddProjectedModuleCommand
        cmd = FitAddProjectedModuleCommand(
            fitID=self.fitID,
            newItemID=self.savedModInfo.itemID,
            newBaseItemID=self.savedModInfo.baseID,
            newMutaplasmidID=self.savedModInfo.mutaplasmidID,
            newMutations=self.savedModInfo.mutations,
            newState=self.savedModInfo.state,
            newChargeID=self.savedModInfo.chargeID,
            newPosition=self.savedModInfo.modPosition)
        cmd.Do()
        return True
