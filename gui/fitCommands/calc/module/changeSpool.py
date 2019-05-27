import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeModuleSpoolCommand(wx.Command):

    def __init__(self, fitID, projected, position, spoolType, spoolAmount):
        wx.Command.__init__(self, True, 'Change Module Spool')
        self.fitID = fitID
        self.projected = projected
        self.position = position
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount
        self.savedSpoolType = None
        self.savedSpoolAmount = None

    def Do(self):
        pyfalog.debug('Doing change of module spoolup at position {} to {} type {} amount on fit {}'.format(self.position, self.spoolType, self.spoolAmount, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        container = fit.modules if not self.projected else fit.projectedModules
        mod = container[self.position]
        if mod.isEmpty:
            pyfalog.warning('Attempt to change spoolup for empty module')
            return False
        self.savedSpoolType = mod.spoolType
        self.savedSpoolAmount = mod.spoolAmount
        if self.spoolType == self.savedSpoolType and self.spoolAmount == self.savedSpoolAmount:
            return False
        mod.spoolType = self.spoolType
        mod.spoolAmount = self.spoolAmount
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of module spoolup at position {} to {} type {} amount on fit {}'.format(self.position, self.spoolType, self.spoolAmount, self.fitID))
        cmd = CalcChangeModuleSpoolCommand(
            fitID=self.fitID,
            projected=self.projected,
            position=self.position,
            spoolType=self.savedSpoolType,
            spoolAmount=self.savedSpoolAmount)
        return cmd.Do()
