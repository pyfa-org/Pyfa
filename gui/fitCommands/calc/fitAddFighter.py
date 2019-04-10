import wx
from logbook import Logger

import eos.db
from eos.saveddata.fighter import Fighter
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitAddFighterCommand(wx.Command):
    """"
    from sFit.addFighter
    """
    def __init__(self, fitID, itemID, state, abilities):
        wx.Command.__init__(self, True, "Add Fighter")
        self.fitID = fitID
        self.newItemID = itemID
        self.newState = state
        self.newAbilities = abilities
        self.newIndex = None

    def Do(self):
        fit = Fit.getInstance().getFit(self.fitID)
        item = Market.getInstance().getItem(self.newItemID, eager=("attributes", "group.category"))
        try:
            fighter = Fighter(item)
        except ValueError:
            pyfalog.warning("Invalid fighter: {}", item)
            return False
        if not fighter.fits(fit):
            return False

        used = fit.getSlotsUsed(fighter.slot)
        total = fit.getNumSlots(fighter.slot)
        if self.newState is not None:
            fighter.active = self.newState
        elif used >= total:
            fighter.active = False
        else:
            fighter.active = True

        if self.newAbilities is not None:
            for ability in fighter.abilities:
                ability.active = self.newAbilities.get(ability.effectID, ability.active)

        fit.fighters.append(fighter)
        self.newIndex = fit.fighters.index(fighter)
        eos.db.commit()
        return True

    def Undo(self):
        from .fitRemoveFighter import FitRemoveFighterCommand  # Avoid circular import
        cmd = FitRemoveFighterCommand(self.fitID, self.newIndex)
        cmd.Do()
        return True
