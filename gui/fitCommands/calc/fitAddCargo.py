import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from eos.saveddata.cargo import Cargo
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitAddCargoCommand(wx.Command):

    def __init__(self, fitID, itemID, amount=1):
        wx.Command.__init__(self, True, 'Add Cargo')
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        pyfalog.debug('Doing addition of cargo {} x{} to fit {}'.format(self.itemID, self.amount, self.fitID))

        fit = Fit.getInstance().getFit(self.fitID)
        item = Market.getInstance().getItem(self.itemID)
        cargo = next((x for x in fit.cargo if x.itemID == self.itemID), None)
        if cargo is None:
            cargo = Cargo(item)
            try:
                fit.cargo.append(cargo)
            except HandledListActionError:
                pyfalog.warning('Failed to append to list')
                eos.db.commit()
                return False
        cargo.amount += self.amount
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of cargo {} x{} to fit {}'.format(self.itemID, self.amount, self.fitID))
        from .fitRemoveCargo import FitRemoveCargoCommand
        cmd = FitRemoveCargoCommand(fitID=self.fitID, itemID=self.itemID, amount=self.amount)
        cmd.Do()
        return True
