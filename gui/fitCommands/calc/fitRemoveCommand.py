import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveCommandCommand(wx.Command):  # well that's an unfortunate name
    """"
    from sFit.removeCommand
    """
    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.savedCommandFitID = commandFitID
        self.savedState = None

    def Do(self):
        pyfalog.debug("Removing command projection from fit ({0}) for: {1}".format(self.fitID, self.savedCommandFitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        commandFit = sFit.getFit(self.savedCommandFitID)
        if not commandFit:
            return False

        commandInfo = commandFit.getCommandInfo(self.fitID)
        if not commandInfo:
            return False

        self.savedState = commandInfo.active

        del fit.commandFitDict[commandFit.ID]

        eos.db.commit()
        return True

    def Undo(self):
        command = eos.db.getFit(self.savedCommandFitID)

        if not command:
            # can't find the command fit, it must have been deleted. Just skip this undo
            return True

        from .fitAddCommand import FitAddCommandCommand
        cmd = FitAddCommandCommand(self.fitID, self.savedCommandFitID, self.savedState)
        cmd.Do()
        return True
