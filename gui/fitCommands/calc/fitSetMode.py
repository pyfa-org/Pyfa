import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitSetModeCommand(wx.Command):
    """"
    from sFit.setMode
    """
    def __init__(self, fitID, mode):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.mode = mode
        self.old_mode = None

    def Do(self):
        pyfalog.debug("Set mode for fit ID: {0}", self.fitID)
        fit = eos.db.getFit(self.fitID)
        self.old_mode = fit.mode
        fit.mode = self.mode
        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitSetModeCommand(self.fitID, self.old_mode)
        cmd.Do()
        return True
