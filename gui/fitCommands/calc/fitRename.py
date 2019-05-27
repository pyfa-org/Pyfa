import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcFitRenameCommand(wx.Command):

    def __init__(self, fitID, name):
        wx.Command.__init__(self, True, 'Rename Fit')
        self.fitID = fitID
        self.name = name
        self.savedName = None

    def Do(self):
        pyfalog.debug('Doing renaming of fit {} to {}'.format(self.fitID, self.name))
        fit = Fit.getInstance().getFit(self.fitID, basic=True)
        if fit.name == self.name:
            return False
        self.savedName = fit.name
        fit.name = self.name
        return True

    def Undo(self):
        pyfalog.debug('Undoing renaming of fit {} to {}'.format(self.fitID, self.name))
        cmd = CalcFitRenameCommand(fitID=self.fitID, name=self.savedName)
        return cmd.Do()
