import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
#from .helpers import ModuleInfoCache
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)
from eos.saveddata.booster import Booster

class FitAddBoosterCommand(wx.Command):
    """"
    from sFit.addBooster
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.new_index = None

    def Do(self):
        pyfalog.debug("Adding booster ({0}) to fit ID: {1}", self.itemID, self.fitID)

        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager="attributes")
        try:
            booster = Booster(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", self.itemID)
            return False

        fit.boosters.append(booster)
        self.new_index = fit.boosters.index(booster)
        return True

    def Undo(self):
        from .fitRemoveBooster import FitRemoveBoosterCommand  # Avoid circular import
        cmd = FitRemoveBoosterCommand(self.fitID, self.new_index)
        cmd.Do()
        return True
