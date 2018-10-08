import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitToggleDroneCommand(wx.Command):
    """"
    from sFit.toggleDrone
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.position = position

    def Do(self):
        pyfalog.debug("Toggling drones for fit ID: {0}", self.fitID)
        fit = eos.db.getFit(self.fitID)
        d = fit.drones[self.position]
        if d.amount == d.amountActive:
            d.amountActive = 0
        else:
            d.amountActive = d.amount

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleDroneCommand(self.fitID, self.position)
        return cmd.Do()
