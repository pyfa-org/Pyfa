import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleProjectedFighterCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Toggle Projected Fighter")
        self.fitID = fitID
        self.position = position

    def Do(self):
        pyfalog.debug("Toggling projected fighter for fit ID: {}".format(self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.projectedFighters[self.position]
        fighter.active = not fighter.active

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleProjectedFighterCommand(self.fitID, self.position)
        return cmd.Do()
