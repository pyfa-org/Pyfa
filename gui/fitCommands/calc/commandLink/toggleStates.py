import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleCommandLinkStatesCommand(wx.Command):

    def __init__(self, fitID, mainLinkID, linkIDs, forceStates=None):
        wx.Command.__init__(self, True, 'Toggle Command Link States')
        self.fitID = fitID
        self.mainLinkID = mainLinkID
        self.linkIDs = linkIDs
        self.forceStates = forceStates
        self.savedStates = None

    def Do(self):
        pyfalog.debug('Doing toggling of command link {}/{} state for fit {}'.format(self.mainLinkID, self.linkIDs, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        if fit is None:
            return False

        linkIDs = self.linkIDs[:]
        if self.mainLinkID not in linkIDs:
            linkIDs.append(self.mainLinkID)

        links = {l.ID: l for l in fit.commandLinks if l.ID in linkIDs}
        if len(links) == 0:
            return False

        self.savedStates = {lid: l.active for lid, l in links.items()}

        mainLink = links.get(self.mainLinkID)
        if self.forceStates is not None:
            for linkID, state in self.forceStates.items():
                link = links.get(linkID)
                if link is not None:
                    link.active = state
        elif mainLink is not None and mainLink.active:
            for link in links.values():
                link.active = False
        elif mainLink is not None and not mainLink.active:
            for link in links.values():
                link.active = True
        else:
            return False
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of command link {}/{} state for fit {}'.format(self.mainLinkID, self.linkIDs, self.fitID))
        cmd = CalcToggleCommandLinkStatesCommand(
            fitID=self.fitID,
            mainLinkID=self.mainLinkID,
            linkIDs=self.linkIDs,
            forceStates=self.savedStates)
        return cmd.Do()
