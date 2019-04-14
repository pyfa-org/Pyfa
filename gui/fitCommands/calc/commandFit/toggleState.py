import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitToggleCommandFitStateCommand(wx.Command):

    def __init__(self, fitID, commandFitID, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Command Fit State')
        self.fitID = fitID
        self.commandFitID = commandFitID
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of command fit {} state for fit {}'.format(self.commandFitID, self.fitID))
        commandFit = Fit.getInstance().getFit(self.commandFitID)
        # Command fit could have been deleted if we are redoing
        if commandFit is None:
            pyfalog.debug('Command fit is not available')
            return False
        commandInfo = commandFit.getCommandInfo(self.fitID)
        if commandInfo is None:
            pyfalog.warning('Fit command info is not available')
            return False
        self.savedState = commandInfo.active
        commandInfo.active = not commandInfo.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of command fit {} state for fit {}'.format(self.commandFitID, self.fitID))
        cmd = FitToggleCommandFitStateCommand(fitID=self.fitID, commandFitID=self.commandFitID, forceState=self.savedState)
        return cmd.Do()
