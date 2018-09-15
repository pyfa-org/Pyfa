import wx
import eos.db
from logbook import Logger
from eos.saveddata.cargo import Cargo
pyfalog = Logger(__name__)


class FitAddCargoCommand(wx.Command):
    """"
    from sFit.addCargo
    """
    def __init__(self, fitID, itemID, amount=1, replace=False):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount  # add x amount. If this goes over amount, removes stack
        self.replace = replace  # if this is false, we increment.

    def Do(self):
        pyfalog.debug("Adding cargo {0} (x{1}) for fit {2}", self.itemID, self.amount, self.fitID)

        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID)

        cargo = next((x for x in fit.cargo if x.itemID == self.itemID), None)

        if cargo is None:
            cargo = Cargo(item)
            fit.cargo.append(cargo)

        if self.replace:
            cargo.amount = self.amount
        else:
            cargo.amount += self.amount

        eos.db.commit()
        return True

    def Undo(self):
        from .fitRemoveCargo import FitRemoveCargoCommand  # Avoid circular import
        cmd = FitRemoveCargoCommand(self.fitID, self.itemID, self.amount)
        cmd.Do()
        return True
