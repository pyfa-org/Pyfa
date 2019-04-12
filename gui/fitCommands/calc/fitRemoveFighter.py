import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import FighterInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveFighterCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Remove Fighter')
        self.fitID = fitID
        self.position = position
        self.savedFighterInfo = None

    def Do(self):
        pyfalog.debug('Doing removal of fighter at position {} from fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        fighter = fit.fighters[self.position]
        self.savedFighterInfo = FighterInfo.fromFighter(fighter)
        fit.fighters.remove(fighter)
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of fighter at position {} from fit {}'.format(self.position, self.fitID))
        from gui.fitCommands.calc.fitAddFighter import FitAddFighterCommand
        cmd = FitAddFighterCommand(fitID=self.fitID, fighterInfo=self.savedFighterInfo, position=self.position)
        return cmd.Do()
