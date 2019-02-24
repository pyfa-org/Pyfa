import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveDroneCommand(wx.Command):
    """"
    from sFit.addDrone
    """
    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True, "Drone add")
        self.fitID = fitID
        self.position = position
        self.amount = amount  # add x amount. If this goes over amount, removes stack
        self.removed_item = None

    def Do(self):
        pyfalog.debug("Removing {0} drones for fit ID: {1}", self.amount, self.fitID)
        fit = eos.db.getFit(self.fitID)
        d = fit.drones[self.position]
        d.amount -= self.amount
        if d.amountActive > 0:
            d.amountActive -= self.amount

        if d.amount == 0:
            self.removed_item = d.itemID
            del fit.drones[self.position]

        eos.db.commit()
        return True

    def Undo(self):
        if self.removed_item:
            from .fitAddDrone import FitAddDroneCommand  # Avoid circular import
            cmd = FitAddDroneCommand(self.fitID, self.removed_item, self.amount)
            return cmd.Do()
        else:
            fit = eos.db.getFit(self.fitID)
            d = fit.drones[self.position]
            d.amount += self.amount
            eos.db.commit()
            return True
