import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
#from .helpers import ModuleInfoCache
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRenameCommand(wx.Command):
    def __init__(self, fitID, newName):
        wx.Command.__init__(self, True, "FitRename")
        self.fitID = fitID
        self.newName = newName
        self.oldName = None

    def Do(self):
        pyfalog.debug("Renaming fit ({0}) to: {1}", self.fitID, self.newName)
        fit = eos.db.getFit(self.fitID)
        self.oldName = fit.name
        fit.name = self.newName
        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitRenameCommand(self.fitID, self.oldName)
        return cmd.Do()
