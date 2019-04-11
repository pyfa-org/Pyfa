import wx
from logbook import Logger

import eos.db
from eos.saveddata.fighter import Fighter
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitAddProjectedFighterCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, itemID, state, abilities):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newItemID = itemID
        self.newState = state
        self.newAbilities = abilities
        self.newIndex = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.newItemID)
        fit = Fit.getInstance().getFit(self.fitID)
        item = Market.getInstance().getItem(self.newItemID, eager=("attributes", "group.category"))

        try:
            fighter = Fighter(item)
        except ValueError:
            return False

        fit.projectedFighters.append(fighter)
        # sometimes fighters aren't added because they aren't valid projectionable ones. todo: move that logic into here
        if fighter not in fit.projectedFighters:
            return False

        if self.newState is not None:
            fighter.active = self.newState

        if self.newAbilities is not None:
            for ability in fighter.abilities:
                ability.active = self.newAbilities.get(ability.effectID, ability.active)

        eos.db.commit()
        self.newIndex = fit.projectedFighters.index(fighter)
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedFighter import FitRemoveProjectedFighterCommand  # avoids circular import
        cmd = FitRemoveProjectedFighterCommand(self.fitID, self.newIndex)
        cmd.Do()
        return True
