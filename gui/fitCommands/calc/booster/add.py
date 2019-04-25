import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddBoosterCommand(wx.Command):

    def __init__(self, fitID, boosterInfo, position=None, commit=True):
        wx.Command.__init__(self, True, 'Add Booster')
        self.fitID = fitID
        self.newBoosterInfo = boosterInfo
        self.newPosition = position
        self.commit = commit
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
                cmd = CalcAddBoosterCommand(
                    fitID=self.fitID,
                    boosterInfo=self.oldBoosterInfo,
                    position=self.oldPosition,
                    commit=self.commit)
                cmd.Do()
                return False
        else:
            try:
                fit.boosters.append(newBooster)
            except HandledListActionError:
                pyfalog.warning('Failed to append to list')
                cmd = CalcAddBoosterCommand(
                    fitID=self.fitID,
                    boosterInfo=self.oldBoosterInfo,
                    position=self.oldPosition,
                    commit=self.commit)
                cmd.Do()
                return False
            self.newPosition = fit.boosters.index(newBooster)

        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undo addition of booster {} to fit {}'.format(self.newBoosterInfo, self.fitID))
        if self.oldBoosterInfo is not None and self.oldPosition is not None:
            cmd = CalcAddBoosterCommand(fitID=self.fitID, boosterInfo=self.oldBoosterInfo, position=self.oldPosition, commit=self.commit)
            return cmd.Do()
        from .remove import CalcRemoveBoosterCommand
        cmd = CalcRemoveBoosterCommand(fitID=self.fitID, position=self.newPosition, commit=self.commit)
        return cmd.Do()
