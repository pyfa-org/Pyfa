import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveProjectedModuleCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.removed_item = None

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}", self.fitID, self.position)
        fit = eos.db.getFit(self.fitID)
        self.removed_item = fit.projectedModules[self.position].itemID
        del fit.projectedModules[self.position]

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedModule import FitAddProjectedModuleCommand
        cmd = FitAddProjectedModuleCommand(self.fitID, self.removed_item)
        cmd.Do()
        return True
