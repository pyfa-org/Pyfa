import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import CargoInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeCargoAmount(wx.Command):

    def __init__(self, fitID, cargoInfo):
        wx.Command.__init__(self, True, 'Change Cargo Quantity')
        self.fitID = fitID
        self.cargoInfo = cargoInfo
        self.savedCargoInfo = None
        self.removeCommand = None

    def Do(self):
        pyfalog.debug('Doing change of cargo {} for fit {}'.format(self.cargoInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cargo = next((c for c in fit.cargo if c.itemID == self.cargoInfo.itemID), None)
        if cargo is None:
            pyfalog.warning('Cannot find cargo item')
            return False
        self.savedCargoInfo = CargoInfo.fromCargo(cargo)
        if self.cargoInfo.amount > 0:
            cargo.amount = self.cargoInfo.amount
            eos.db.commit()
            return True
        else:
            from .fitRemoveCargo import FitRemoveCargoCommand
            self.removeCommand = FitRemoveCargoCommand(fitID=self.fitID, cargoInfo=self.savedCargoInfo)
            return self.removeCommand.Do()

    def Undo(self):
        pyfalog.debug('Undoing change of cargo {} for fit {}'.format(self.cargoInfo, self.fitID))
        if self.removeCommand is not None:
            return self.removeCommand.Undo()
        cmd = FitChangeCargoAmount(self.fitID, self.savedCargoInfo)
        return cmd.Do()
