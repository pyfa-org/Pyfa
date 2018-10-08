import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveImplantCommand(wx.Command):
    """"
    Fitting command that sets the amount for an item within the cargo.

    from sFit.removeImplant
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Implant remove")
        self.fitID = fitID
        self.position = position
        self.old_implant = None

    def Do(self):
        pyfalog.debug("Removing implant from position ({0}) for fit ID: {1}", self.position, self.fitID)

        fit = eos.db.getFit(self.fitID)
        implant = fit.implants[self.position]
        self.old_implant = implant.itemID
        fit.implants.remove(implant)
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddImplant import FitAddImplantCommand  # Avoid circular import
        cmd = FitAddImplantCommand(self.fitID, self.old_implant)
        cmd.Do()
        return True
