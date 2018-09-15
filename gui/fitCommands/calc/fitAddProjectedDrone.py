import wx
import eos.db
from logbook import Logger
from eos.saveddata.drone import Drone
pyfalog = Logger(__name__)


class FitAddProjectedDroneCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.index = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.itemID)
        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID)

        drone = None
        for d in fit.projectedDrones.find(item):
            if d is None or d.amountActive == d.amount or d.amount >= 5:
                drone = d
                break

        if drone is None:
            drone = Drone(item)
            if not drone.item.isType("projected"):
                return False
            fit.projectedDrones.append(drone)

        self.index = fit.projectedDrones.index(drone)
        drone.amount += 1

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedDrone import FitRemoveProjectedDroneCommand  # avoids circular import
        cmd = FitRemoveProjectedDroneCommand(self.fitID, self.index)
        cmd.Do()
        return True
