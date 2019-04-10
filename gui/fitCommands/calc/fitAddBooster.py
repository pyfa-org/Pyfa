import wx
import eos.db
from logbook import Logger
from eos.saveddata.booster import Booster
pyfalog = Logger(__name__)


class FitAddBoosterCommand(wx.Command):
    """"
    from sFit.addBooster
    """
    def __init__(self, fitID, itemID, state, sideEffects):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newItemID = itemID
        self.newState = state
        self.newSideEffects = sideEffects
        self.newIndex = None
        self.oldItemID = None
        self.oldState = None
        self.oldSideEffects = None

    def Do(self):
        pyfalog.debug("Adding booster ({0}) to fit ID: {1}", self.newItemID, self.fitID)

        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.newItemID, eager="attributes")

        if next((x for x in fit.boosters if x.itemID == self.newItemID), None):
            return False  # already have item in list of boosters

        try:
            booster = Booster(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", self.newItemID)
            return False

        if self.newState is not None:
            booster.active = self.newState
        if self.newSideEffects is not None:
            for sideEffect in booster.sideEffects:
                sideEffect.active = self.newSideEffects.get(sideEffect.effectID, False)


        self.oldItemID, self.oldState, self.oldSideEffects = fit.boosters.makeRoom(booster)
        fit.boosters.append(booster)
        self.newIndex = fit.boosters.index(booster)
        return True

    def Undo(self):
        if self.oldItemID:
            # If we had an item in the slot previously, add it back.
            cmd = FitAddBoosterCommand(self.fitID, self.oldItemID, self.oldState, self.oldSideEffects)
            cmd.Do()
            return True

        from .fitRemoveBooster import FitRemoveBoosterCommand  # Avoid circular import
        cmd = FitRemoveBoosterCommand(self.fitID, self.newIndex)
        cmd.Do()
        return True
