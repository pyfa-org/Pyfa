import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitAddCommandCommand(wx.Command):  # well that's an unfrtunate name
    """"
    from sFit.addCommand
    """
    def __init__(self, fitID, commandFitID, state):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.commandFitID = commandFitID
        self.state = state

    def Do(self):
        pyfalog.debug("Projecting command fit ({0}) onto: {1}".format(self.fitID, self.commandFitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        commandFit = sFit.getFit(self.commandFitID)

        if not commandFit:
            # if redoing when the command fit has been deleted, simply fail this command
            return False

        if commandFit in fit.commandFits:
            return False

        fit.commandFitDict[commandFit.ID] = commandFit

        # this bit is required -- see GH issue # 83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(commandFit)

        if self.state is not None:
            commandInfo = commandFit.getCommandInfo(self.fitID)
            if not commandInfo:
                return False
            commandInfo.active = self.state

        eos.db.commit()
        return True

    def Undo(self):
        command = eos.db.getFit(self.commandFitID)

        if not command:
            # can't find the command fit, it must have been deleted. Just skip this undo
            return True

        from .fitRemoveCommand import FitRemoveCommandCommand
        cmd = FitRemoveCommandCommand(self.fitID, self.commandFitID)
        cmd.Do()
        return True
