import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveBoosterCommand(wx.Command):
    """"
    from sFit.removeBooster
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Implant remove")
        self.fitID = fitID
        self.position = position
        self.savedItemID = None
        self.savedState = None
        self.savedSideEffects = None

    def Do(self):
        pyfalog.debug("Removing booster from position ({0}) for fit ID: {1}", self.position, self.fitID)

        fit = eos.db.getFit(self.fitID)
        booster = fit.boosters[self.position]
        self.savedItemID = booster.itemID
        self.savedState = booster.active
        self.savedSideEffects = {se.effectID: se.active for se in booster.sideEffects}
        fit.boosters.remove(booster)
        return True

    def Undo(self):
        from .fitAddBooster import FitAddBoosterCommand  # Avoid circular import
        cmd = FitAddBoosterCommand(
            fitID=self.fitID,
            itemID=self.savedItemID,
            state=self.savedState,
            sideEffects=self.savedSideEffects)
        cmd.Do()
        return True
