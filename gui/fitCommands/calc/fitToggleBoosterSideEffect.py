import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleBoosterSideEffectCommand(wx.Command):

    def __init__(self, fitID, position, effectID):
        wx.Command.__init__(self, True, "Toggle Booster Side Effect")
        self.fitID = fitID
        self.position = position
        self.effectID = effectID

    def Do(self):
        pyfalog.debug("Toggling booster side-effect for fit ID: {0}", self.fitID)
        fit = Fit.getInstance().getFit(self.fitID)
        booster = fit.boosters[self.position]
        for se in booster.sideEffects:
            if se.effectID == self.effectID:
                sideEffect = se
                break
        else:
            return False

        sideEffect.active = not sideEffect.active
        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleBoosterSideEffectCommand(self.fitID, self.position, self.effectID)
        return cmd.Do()
