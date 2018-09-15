import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveCargoCommand(wx.Command):
    """"
    Fitting command that sets the amount for an item within the cargo.

    from sFit.removeCargo
    """
    def __init__(self, fitID, itemID, amount=1, stack=False):
        wx.Command.__init__(self, True, "Cargo remove")
        self.fitID = fitID
        self.itemID = itemID
        self.stack = stack  # remove entire stack
        self.amount = amount  # remove x amount. If this goes over amount, removes stack
        self.old_amount = None

    def Do(self):
        pyfalog.debug("Removing cargo {0} (x{1}) for fit {2}", self.itemID, self.amount, self.fitID)
        fit = eos.db.getFit(self.fitID)
        cargo = next((x for x in fit.cargo if x.itemID == self.itemID), None)

        if cargo is None:
            return False

        self.old_amount = cargo.amount

        if self.amount >= cargo.amount:
            self.stack = True  # set to full stack, this allows easier logic in the Undo function

        if self.stack or self.amount >= cargo.amount:
            fit.cargo.remove(cargo)
            eos.db.commit()
            return True

        cargo.amount -= self.amount
        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddCargo import FitAddCargoCommand  # Avoid circular import
        cmd = FitAddCargoCommand(self.fitID, self.itemID, self.old_amount, True)
        cmd.Do()
        return True
