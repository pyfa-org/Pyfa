import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitRemoveCommandCommand(wx.Command):  # well that's an unfortunate name
    """"
    from sFit.removeCommand
    """
    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.commandFitID = commandFitID

    def Do(self):
        pyfalog.debug("Removing command projection from fit ({0}) for: {1}", self.fitID, self.commandFitID)
        fit = eos.db.getFit(self.fitID)
        command = eos.db.getFit(self.commandFitID)
        if not command:
            return False
        del fit.commandFitDict[command.ID]

        eos.db.commit()
        return True

    def Undo(self):
        command = eos.db.getFit(self.commandFitID)

        if not command:
            # can't find the command fit, it must have been deleted. Just skip this undo
            return True

        from .fitAddCommand import FitAddCommandCommand
        cmd = FitAddCommandCommand(self.fitID, self.commandFitID)
        cmd.Do()
        return True
