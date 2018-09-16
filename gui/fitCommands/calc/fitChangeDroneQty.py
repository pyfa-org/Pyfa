import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitChangeDroneQty(wx.Command):
    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True, "Drone add")
        self.fitID = fitID
        self.position = position
        self.amount = amount  # add x amount. If this goes over amount, removes stack
        self.old_amount = None

    def Do(self):
        pyfalog.debug("Changing active fighters ({0}) for fit ({1}) to amount: {2}", self.position, self.fitID, self.amount)
        fit = eos.db.getFit(self.fitID)
        drone = fit.drones[self.position]
        self.old_amount = drone.amount
        drone.amount = self.amount

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitChangeDroneQty(self.fitID, self.position, self.old_amount)
        return cmd.Do()
