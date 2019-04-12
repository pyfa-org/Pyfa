import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddBoosterCommand(wx.Command):

    def __init__(self, fitID, newBoosterInfo, newPosition=None):
        wx.Command.__init__(self, True, 'Add Booster')
        self.fitID = fitID
        self.newBoosterInfo = newBoosterInfo
        self.newPosition = newPosition
        self.oldBoosterInfo = None
        self.oldPosition = None

    def Do(self):
        pyfalog.debug('Doing addition of booster {} to fit {}'.format(self.newBoosterInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        if any(self.newBoosterInfo.itemID == b.itemID for b in fit.boosters):
            pyfalog.debug('Skipping as such booster is already on the fit')
            return False

        newBooster = self.newBoosterInfo.toBooster()
        if newBooster is None:
            return False

        self.oldPosition, self.oldBoosterInfo = fit.boosters.makeRoom(newBooster)

        if self.newPosition is not None:
            try:
                fit.boosters.insert(self.newPosition, newBooster)
            except HandledListActionError:
                pyfalog.warning('Failed to insert to list')
                cmd = FitAddBoosterCommand(
                    fitID=self.fitID,
                    newBoosterInfo=self.oldBoosterInfo,
                    newPosition=self.oldPosition)
                cmd.Do()
                return False
        else:
            try:
                fit.boosters.append(newBooster)
            except HandledListActionError:
                pyfalog.warning('Failed to append to list')
                cmd = FitAddBoosterCommand(
                    fitID=self.fitID,
                    newBoosterInfo=self.oldBoosterInfo,
                    newPosition=self.oldPosition)
                cmd.Do()
                return False
            self.newPosition = fit.boosters.index(newBooster)

        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undo addition of booster {} to fit {}'.format(self.newBoosterInfo, self.fitID))
        if self.oldBoosterInfo and self.oldPosition:
            cmd = FitAddBoosterCommand(
                fitID=self.fitID,
                newBoosterInfo=self.oldBoosterInfo,
                newPosition=self.oldPosition)
            return cmd.Do()
        from .fitRemoveBooster import FitRemoveBoosterCommand
        cmd = FitRemoveBoosterCommand(self.fitID, self.newPosition)
        return cmd.Do()
