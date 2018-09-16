import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitToggleBoosterCommand(wx.Command):
    """"
    from sFit.toggleBooster
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.position = position

    def Do(self):
        pyfalog.debug("Toggling booster for fit ID: {0}", self.fitID)
        fit = eos.db.getFit(self.fitID)
        booster = fit.boosters[self.position]
        booster.active = not booster.active

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleBoosterCommand(self.fitID, self.position)
        return cmd.Do()
