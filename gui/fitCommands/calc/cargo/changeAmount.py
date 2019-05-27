import wx
from logbook import Logger

from gui.fitCommands.helpers import CargoInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeCargoAmountCommand(wx.Command):

    def __init__(self, fitID, cargoInfo):
        wx.Command.__init__(self, True, 'Change Cargo Amount')
        self.fitID = fitID
        self.cargoInfo = cargoInfo
        self.savedCargoInfo = None

    def Do(self):
        pyfalog.debug('Doing change of cargo {} for fit {}'.format(self.cargoInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cargo = next((c for c in fit.cargo if c.itemID == self.cargoInfo.itemID), None)
        if cargo is None:
            pyfalog.warning('Cannot find cargo item')
            return False
        self.savedCargoInfo = CargoInfo.fromCargo(cargo)
        if self.cargoInfo.amount == self.savedCargoInfo.amount:
            return False
        cargo.amount = self.cargoInfo.amount
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of cargo {} for fit {}'.format(self.cargoInfo, self.fitID))
        cmd = CalcChangeCargoAmountCommand(fitID=self.fitID, cargoInfo=self.savedCargoInfo)
        return cmd.Do()
