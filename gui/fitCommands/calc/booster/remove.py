import wx
from logbook import Logger

from gui.fitCommands.helpers import BoosterInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveBoosterCommand(wx.Command):

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
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of booster {} on fit {}'.format(self.savedBoosterInfo, self.fitID))
        from .add import CalcAddBoosterCommand
        cmd = CalcAddBoosterCommand(
            fitID=self.fitID,
            boosterInfo=self.savedBoosterInfo,
            position=self.position)
        return cmd.Do()
