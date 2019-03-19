import wx
import eos.db
from logbook import Logger
from eos.saveddata.booster import Booster
pyfalog = Logger(__name__)


class FitSetSpoolupCommand(wx.Command):
    def __init__(self, fitID, position, spoolType, spoolAmount):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount
        self.projected = False # todo: get this to work with projected modules? Is that a thing?
        self.cache = None

    def Do(self):
        return self.__set(self.spoolType, self.spoolAmount)

    def Undo(self):
        if self.cache:
            self.__set(*self.cache)
        return True

    def __set(self, type, amount):
        fit = eos.db.getFit(self.fitID)
        source = fit.modules if not self.projected else fit.projectedModules

        mod = source[self.position]
        self.cache = mod.spoolType, mod.spoolAmount

        mod.spoolType = type
        mod.spoolAmount = amount

        eos.db.commit()
        return True
