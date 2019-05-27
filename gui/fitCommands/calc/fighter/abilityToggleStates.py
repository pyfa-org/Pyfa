import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleFighterAbilityStatesCommand(wx.Command):

    def __init__(self, fitID, projected, mainPosition, positions, effectID, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Fighter Ability States')
        self.fitID = fitID
        self.projected = projected
        self.mainPosition = mainPosition
        self.positions = positions
        self.effectID = effectID
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of fighter ability {} state at position {}/{} for fit {}'.format(self.effectID, self.mainPosition, self.positions, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        container = fit.projectedFighters if self.projected else fit.fighters

        positions = self.positions[:]
        if self.mainPosition not in positions:
            positions.append(self.mainPosition)
        savedStates = {}
        for position in positions:
            fighter = container[position]
            ability = next((fa for fa in fighter.abilities if fa.effectID == self.effectID), None)
            if ability is None:
                continue
            savedStates[position] = ability.active
        if len(savedStates) > 0:
            self.savedStates = savedStates

        mainFighter = container[self.mainPosition]
        mainAbility = next((fa for fa in mainFighter.abilities if fa.effectID == self.effectID), None)

        changes = False
        if self.forceStates is not None:
            for position, state in self.forceStates.items():
                fighter = container[position]
                ability = next((fa for fa in fighter.abilities if fa.effectID == self.effectID), None)
                if ability is None:
                    continue
                changes = True
                if ability.active is not state:
                    ability.active = state
        elif mainAbility is None:
            pyfalog.warning('Unable to find main fighter ability')
            return False
        elif mainAbility.active:
            for position in positions:
                fighter = container[position]
                ability = next((fa for fa in fighter.abilities if fa.effectID == self.effectID), None)
                if ability is None:
                    continue
                if ability.active:
                    changes = True
                    ability.active = False
        else:
            for position in positions:
                fighter = container[position]
                ability = next((fa for fa in fighter.abilities if fa.effectID == self.effectID), None)
                if ability is None:
                    continue
                if not ability.active:
                    changes = True
                    ability.active = True
        return changes

    def Undo(self):
        pyfalog.debug('Undoing toggling of fighter ability {} state at position {}/{} for fit {}'.format(self.effectID, self.mainPosition, self.positions, self.fitID))
        cmd = CalcToggleFighterAbilityStatesCommand(
            fitID=self.fitID,
            projected=self.projected,
            mainPosition=self.mainPosition,
            positions=self.positions,
            effectID=self.effectID,
            forceStates=self.savedStates)
        return cmd.Do()
