import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddCargoCommand(wx.Command):

    def __init__(self, fitID, cargoInfo, commit=True):
        wx.Command.__init__(self, True, 'Add Cargo')
        self.fitID = fitID
        self.cargoInfo = cargoInfo
        self.commit = commit

    def Do(self):
        pyfalog.debug('Doing addition of cargo {} to fit {}'.format(self.cargoInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cargo = next((c for c in fit.cargo if c.itemID == self.cargoInfo.itemID), None)
        if cargo is not None:
            cargo.amount += self.cargoInfo.amount
        else:
            cargo = self.cargoInfo.toCargo()
            fit.cargo.append(cargo)
            if cargo not in fit.cargo:
                pyfalog.warning('Failed to append to list')
                if self.commit:
                    eos.db.commit()
                return False
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of cargo {} to fit {}'.format(self.cargoInfo, self.fitID))
        from .remove import CalcRemoveCargoCommand
        cmd = CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=self.cargoInfo, commit=self.commit)
        return cmd.Do()
