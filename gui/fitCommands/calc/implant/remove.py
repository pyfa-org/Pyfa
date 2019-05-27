import wx
from logbook import Logger

from gui.fitCommands.helpers import ImplantInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveImplantCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Remove Implant')
        self.fitID = fitID
        self.position = position
        self.savedImplantInfo = None

    def Do(self):
        pyfalog.debug('Doing removal of implant from position {} on fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        implant = fit.implants[self.position]
        self.savedImplantInfo = ImplantInfo.fromImplant(implant)
        fit.implants.remove(implant)
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of implant {} on fit {}'.format(self.savedImplantInfo, self.fitID))
        from .add import CalcAddImplantCommand
        cmd = CalcAddImplantCommand(
            fitID=self.fitID,
            implantInfo=self.savedImplantInfo,
            position=self.position)
        return cmd.Do()
