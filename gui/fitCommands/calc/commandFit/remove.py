import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveCommandFitCommand(wx.Command):

    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True, 'Remove Command Fit')
        self.fitID = fitID
        self.commandFitID = commandFitID
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing removal of command fit {} for fit {}'.format(self.commandFitID, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        commandFit = sFit.getFit(self.commandFitID)

        # Can be removed by the time we're redoing it
        if commandFit is None:
            pyfalog.debug('Command fit is not available')
            return False
        commandInfo = commandFit.getCommandInfo(self.fitID)
        if commandInfo is None:
            pyfalog.warning('Fit command info is not available')
            return False
        self.savedState = commandInfo.active
        if commandFit.ID not in fit.commandFitDict:
            pyfalog.warning('Unable to find commanding fit in command dict')
            return False
        del fit.commandFitDict[commandFit.ID]
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of command fit {} for fit {}'.format(self.commandFitID, self.fitID))
        from .add import CalcAddCommandCommand
        cmd = CalcAddCommandCommand(
            fitID=self.fitID,
            commandFitID=self.commandFitID,
            state=self.savedState)
        return cmd.Do()
