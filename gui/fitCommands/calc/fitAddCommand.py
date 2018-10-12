import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitAddCommandCommand(wx.Command):  # well that's an unfrtunate name
    """"
    from sFit.addCommand
    """
    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.commandFitID = commandFitID

    def Do(self):
        pyfalog.debug("Projecting command fit ({0}) onto: {1}", self.fitID, self.commandFitID)
        fit = eos.db.getFit(self.fitID)
        command = eos.db.getFit(self.commandFitID)

        if not command:
            # if redoing when the command fit has been deleted, simply fail this command
            return False

        if command in fit.commandFits:
            return

        fit.commandFitDict[command.ID] = command

        # this bit is required -- see GH issue # 83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(command)

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
