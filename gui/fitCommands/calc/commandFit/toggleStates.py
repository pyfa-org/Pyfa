import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleCommandFitStatesCommand(wx.Command):

    def __init__(self, fitID, mainCommandFitID, commandFitIDs, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Command Fit States')
        self.fitID = fitID
        self.mainCommandFitID = mainCommandFitID
        self.commandFitIDs = commandFitIDs
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of command fit {}/{} state for fit {}'.format(self.mainCommandFitID, self.commandFitIDs, self.fitID))
        sFit = Fit.getInstance()

        commandFitIDs = self.commandFitIDs[:]
        if self.mainCommandFitID not in commandFitIDs:
            commandFitIDs.append(self.mainCommandFitID)

        commandInfos = {}
        for commandFitID in commandFitIDs:
            commandFit = sFit.getFit(commandFitID)
            # Command fit could have been deleted if we are redoing
            if commandFit is None:
                pyfalog.debug('Command fit is not available')
                continue
            commandInfo = commandFit.getCommandInfo(self.fitID)
            if commandInfo is None:
                pyfalog.warning('Fit command info is not available')
                continue
            commandInfos[commandFitID] = commandInfo

        if len(commandInfos) == 0:
            return False

        self.savedStates = {cfid: ci.active for cfid, ci in commandInfos.items()}

        mainCommandInfo = commandInfos.get(self.mainCommandFitID)
        if self.forceStates is not None:
            for commandFitID, state in self.forceStates.items():
                commandInfo = commandInfos.get(commandFitID)
                if commandInfo is None:
                    continue
                commandInfo.active = state
        elif mainCommandInfo is not None and mainCommandInfo.active:
            for commandInfo in commandInfos.values():
                commandInfo.active = False
        elif mainCommandInfo is not None and not mainCommandInfo.active:
            for commandInfo in commandInfos.values():
                commandInfo.active = True
        # Bail if we cannot calculate which state to take
        else:
            return False
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of command fit {}/{} state for fit {}'.format(self.mainCommandFitID, self.commandFitIDs, self.fitID))
        cmd = CalcToggleCommandFitStatesCommand(
            fitID=self.fitID,
            mainCommandFitID=self.mainCommandFitID,
            commandFitIDs=self.commandFitIDs,
            forceStates=self.savedStates)
        return cmd.Do()
