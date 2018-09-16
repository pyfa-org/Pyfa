import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitToggleCommandCommand(wx.Command):
    """"
    from sFit.toggleCommandFit
    """
    def __init__(self, fitID, commandFitId):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.commandFitID = commandFitId

    def Do(self):
        pyfalog.debug("Toggle command fit ({0}) for: {1}", self.commandFitID, self.fitID)
        commandFit = eos.db.getFit(self.commandFitID)

        if not commandFit:
            pyfalog.debug(" -- Command fit not found, deleted?")
            return False

        commandInfo = commandFit.getCommandInfo(self.fitID)

        if not commandInfo:
            pyfalog.debug(" -- Command fit info not found, deleted?")
            return False

        commandInfo.active = not commandInfo.active
        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitToggleCommandCommand(self.fitID, self.commandFitID)
        return cmd.Do()
