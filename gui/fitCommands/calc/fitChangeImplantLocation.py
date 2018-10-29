import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitChangeImplantLocation(wx.Command):
    def __init__(self, fitID, source):
        wx.Command.__init__(self, True, "Drone add")
        self.fitID = fitID
        self.source = source
        self.old_source = None

    def Do(self):
        pyfalog.debug("Toggling implant source for fit ID: {0}", self.fitID)
        fit = eos.db.getFit(self.fitID)
        self.old_source = fit.implantSource
        fit.implantSource = self.source
        eos.db.commit()
        return True


    def Undo(self):
        cmd = FitChangeImplantLocation(self.fitID, self.old_source)
        return cmd.Do()
