import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


# this has the same exact definition that regular projected modules, besides the undo
class FitRemoveProjectedDroneCommand(wx.Command):
    """"
    from sFit.project
    """

    def __init__(self, fitID, position, stack=False):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.removed_item = None
        self.stack = stack

    def Do(self):
        pyfalog.debug("Removing ({0}) onto: {1}", self.fitID, self.position)
        fit = eos.db.getFit(self.fitID)

        drone = fit.projectedDrones[self.position]
        if self.stack:
            fit.projectedDrones.remove(drone)
        else:
            if drone.amount > 1:
                drone.amount -= 1
            else:
                fit.projectedDrones.remove(drone)

        self.drone_item = drone.itemID

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddProjectedDrone import FitAddProjectedDroneCommand
        cmd = FitAddProjectedDroneCommand(self.fitID, self.drone_item)
        cmd.Do()
        return True
