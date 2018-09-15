import wx
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitAddProjectedEnvCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.new_index = None
        self.old_item = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.itemID)
        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager=("attributes", "group.category"))

        try:
            module = Module(item)
        except ValueError:
            return False

        # todo: thing to check for existing environmental effects

        self.old_item = fit.projectedModules.makeRoom(module)

        module.state = State.ONLINE
        fit.projectedModules.append(module)

        eos.db.commit()
        self.new_index = fit.projectedModules.index(module)
        return True

    def Undo(self):
        if self.old_item:
            # If we had an item in the slot previously, add it back.
            cmd = FitAddProjectedEnvCommand(self.fitID, self.old_item)
            cmd.Do()
            return True
        from gui.fitCommands.calc.fitRemoveProjectedEnv import FitRemoveProjectedEnvCommand  # avoids circular import
        cmd = FitRemoveProjectedEnvCommand(self.fitID, self.itemID)
        cmd.Do()

        return True
