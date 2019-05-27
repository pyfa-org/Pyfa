import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleBoosterSideEffectStateCommand(wx.Command):

    def __init__(self, fitID, position, effectID, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Booster Side Effect State')
        self.fitID = fitID
        self.position = position
        self.effectID = effectID
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of booster side effect {} state at position {} for fit {}'.format(self.effectID, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        booster = fit.boosters[self.position]
        sideEffect = next((se for se in booster.sideEffects if se.effectID == self.effectID), None)
        if sideEffect is None:
            pyfalog.warning('Unable to find booster side effect')
            return False
        self.savedState = sideEffect.active
        sideEffect.active = not sideEffect.active if self.forceState is None else self.forceState
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of booster side effect {} state at position {} for fit {}'.format(self.effectID, self.position, self.fitID))
        cmd = CalcToggleBoosterSideEffectStateCommand(fitID=self.fitID, position=self.position, effectID=self.effectID, forceState=self.savedState)
        return cmd.Do()
