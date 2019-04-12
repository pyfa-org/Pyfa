import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddCargoCommand(wx.Command):

    def __init__(self, fitID, cargoInfo):
        wx.Command.__init__(self, True, 'Add Cargo')
        self.fitID = fitID
        self.cargoInfo = cargoInfo

    def Do(self):
        pyfalog.debug('Doing addition of cargo {} to fit {}'.format(self.cargoInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cargo = next((x for x in fit.cargo if x.itemID == self.cargoInfo.itemID), None)
        if cargo is None:
            cargo = self.cargoInfo.toCargo()
            try:
                fit.cargo.append(cargo)
            except HandledListActionError:
                pyfalog.warning('Failed to append to list')
                eos.db.commit()
                return False
        else:
            cargo.amount += self.cargoInfo.amount
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of cargo {} to fit {}'.format(self.cargoInfo, self.fitID))
        from .fitRemoveCargo import FitRemoveCargoCommand
        cmd = FitRemoveCargoCommand(fitID=self.fitID, cargoInfo=self.cargoInfo)
        cmd.Do()
        return True
