import wx
import eos.db
from logbook import Logger
from eos.saveddata.module import Module, State
pyfalog = Logger(__name__)


class FitAddProjectedModuleCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.new_index = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.itemID)
        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager=("attributes", "group.category"))

        try:
            module = Module(item)
            if not module.item.isType("projected"):
                return False
        except ValueError:
            return False

        module.state = State.ACTIVE
        if not module.canHaveState(module.state, fit):
            module.state = State.OFFLINE
        fit.projectedModules.append(module)

        eos.db.commit()
        self.new_index = fit.projectedModules.index(module)
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedModule import FitRemoveProjectedModuleCommand  # avoids circular import
        cmd = FitRemoveProjectedModuleCommand(self.fitID, self.new_index)
        cmd.Do()
        return True
