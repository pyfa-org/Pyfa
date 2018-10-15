import wx
from logbook import Logger

import eos.db
pyfalog = Logger(__name__)


class FitChangeDroneVariationCommand(wx.Command):
    """"
    Fitting command that changes an existing drone into another variation.
    """
    def __init__(self, fitID, position, itemID):
        wx.Command.__init__(self, True, "Change Module")

        self.fitID = fitID
        self.itemID = itemID
        self.position = position
        self.old_drone = None

    def Do(self):
        return self.change_drone(self.fitID, self.position, self.itemID)

    def Undo(self):
        self.change_drone(self.fitID, self.position, self.old_drone)
        return True

    def change_drone(self, fitID, position, itemID):
        fit = eos.db.getFit(self.fitID)
        drone = fit.drones[self.position]

        if itemID == drone.itemID:
            return False

        self.old_drone = drone.itemID

        drone.changeType(itemID)
        eos.db.commit()
        # todo: ensure that, whatever type we send in, is actually a variation of the original drone. If not, return False
        return True
