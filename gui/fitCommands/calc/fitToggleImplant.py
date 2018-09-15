import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitToggleImplantCommand(wx.Command):
    """"
    from sFit.toggleImplant
    """
    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.position = position

    def Do(self):
        pyfalog.debug("Toggling implant for fit ID: {0}", self.fitID)
        fit = eos.db.getFit(self.fitID)
        implant = fit.implants[self.position]
        implant.active = not implant.active

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleImplantCommand(self.fitID, self.position)
        return cmd.Do()
