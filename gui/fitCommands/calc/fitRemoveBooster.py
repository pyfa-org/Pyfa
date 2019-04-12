import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import BoosterInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveBoosterCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Remove Booster')
        self.fitID = fitID
        self.position = position
        self.savedBoosterInfo = None

    def Do(self):
        pyfalog.debug('Doing removal of booster from position {} on fit {}'.format(self.position, self.fitID))

        fit = Fit.getInstance().getFit(self.fitID)
        booster = fit.boosters[self.position]
        self.savedBoosterInfo = BoosterInfo.fromBooster(booster)
        fit.boosters.remove(booster)
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of booster {} on fit {}'.format(self.savedBoosterInfo, self.fitID))
        from .fitAddBooster import FitAddBoosterCommand  # Avoid circular import
        cmd = FitAddBoosterCommand(
            fitID=self.fitID,
            boosterInfo=self.savedBoosterInfo,
            position=self.position)
        return cmd.Do()
