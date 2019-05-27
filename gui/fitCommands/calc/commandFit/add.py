import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddCommandCommand(wx.Command):

    def __init__(self, fitID, commandFitID, state=None):
        wx.Command.__init__(self, True, 'Add Command Fit')
        self.fitID = fitID
        self.commandFitID = commandFitID
        self.state = state

    def Do(self):
        pyfalog.debug('Doing addition of command fit {} for fit {}'.format(self.commandFitID, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        commandFit = sFit.getFit(self.commandFitID)

        # Command fit could have been deleted if we are redoing
        if commandFit is None:
            pyfalog.debug('Command fit is not available')
            return False
        # Already commanding this ship
        if commandFit in fit.commandFits:
            pyfalog.debug('Command fit had been applied already')
            return False
        if commandFit.ID in fit.commandFitDict:
            pyfalog.debug('Commanding fit is in command dict already')
            return False
        fit.commandFitDict[commandFit.ID] = commandFit
        # This bit is required, see issue #83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(commandFit)

        if self.state is not None:
            fitCommandInfo = commandFit.getCommandInfo(self.fitID)
            if fitCommandInfo is None:
                pyfalog.warning('Fit command info is not available')
                self.Undo()
                return False
            fitCommandInfo.active = self.state

        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of command fit {} for fit {}'.format(self.commandFitID, self.fitID))
        # Can't find the command fit, it must have been deleted. Just skip, as deleted fit
        # means that someone else just did exactly what we wanted to do
        commandFit = Fit.getInstance().getFit(self.commandFitID)
        if commandFit is None:
            return True
        from .remove import CalcRemoveCommandFitCommand
        cmd = CalcRemoveCommandFitCommand(fitID=self.fitID, commandFitID=self.commandFitID)
        return cmd.Do()
