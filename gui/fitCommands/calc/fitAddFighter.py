import wx
import eos.db
from logbook import Logger
from eos.saveddata.fighter import Fighter
pyfalog = Logger(__name__)


class FitAddFighterCommand(wx.Command):
    """"
    from sFit.addFighter
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.itemID = itemID
        self.new_index = None

    def Do(self):
        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager=("attributes", "group.category"))

        try:
            fighter = Fighter(item)
        except ValueError:
            pyfalog.warning("Invalid fighter: {}", item)
            return False

        if not fighter.fits(fit):
            return False

        used = fit.getSlotsUsed(fighter.slot)
        total = fit.getNumSlots(fighter.slot)

        if used >= total:
            fighter.active = False

        fit.fighters.append(fighter)
        self.new_index = fit.fighters.index(fighter)

        eos.db.commit()

        return True

    def Undo(self):
        from .fitRemoveFighter import FitRemoveFighterCommand  # Avoid circular import
        cmd = FitRemoveFighterCommand(self.fitID, self.new_index)
        cmd.Do()
        return True
