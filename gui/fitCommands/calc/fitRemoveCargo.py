import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveCargoCommand(wx.Command):

    def __init__(self, fitID, itemID, amount=1):
        wx.Command.__init__(self, True, 'Remove Cargo')
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount  # Pass infinity if you want to remove stack
        self.savedRemovedAmount = None

    def Do(self):
        pyfalog.debug('Doing removal of cargo {} x{} from fit {}'.format(self.itemID, self.amount, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cargo = next((x for x in fit.cargo if x.itemID == self.itemID), None)
        if cargo is None:
            return False

        self.savedRemovedAmount = min(cargo.amount, self.amount)

        cargo.amount -= self.savedRemovedAmount
        if cargo.amount <= 0:
            fit.cargo.remove(cargo)

        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of cargo {} x{} from fit {}'.format(self.itemID, self.amount, self.fitID))
        from gui.fitCommands.calc.fitAddCargo import FitAddCargoCommand
        cmd = FitAddCargoCommand(fitID=self.fitID, itemID=self.itemID, amount=self.savedRemovedAmount)
        return cmd.Do()
