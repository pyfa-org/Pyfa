import wx
import eos.db
from logbook import Logger
from .fitRemoveProjectedModule import FitRemoveProjectedModuleCommand
pyfalog = Logger(__name__)


# this has the same exact definition that regular rpojected modules, besides the undo
class FitRemoveProjectedEnvCommand(FitRemoveProjectedModuleCommand):
    """"
    from sFit.project
    """

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.removed_item = None

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}", self.fitID, self.itemID)
        fit = eos.db.getFit(self.fitID)

        item = next((x for x in fit.projectedModules if x.itemID == self.itemID), None)
        self.removed_item = item.itemID
        fit.projectedModules.remove(item)

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedEnv import FitAddProjectedEnvCommand
        cmd = FitAddProjectedEnvCommand(self.fitID, self.removed_item)
        cmd.Do()
        return True
