import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveCommandLinkCommand(wx.Command):

    def __init__(self, fitID, linkID):
        wx.Command.__init__(self, True, 'Remove Command Link')
        self.fitID = fitID
        self.linkID = linkID
        self.savedLinkType = None
        self.savedStrength = None
        self.savedMindlink = None
        self.savedActive = None

    def Do(self):
        pyfalog.debug('Doing removal of command link {} for fit {}'.format(self.linkID, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        if fit is None:
            return False
        link = next((l for l in fit.commandLinks if l.ID == self.linkID), None)
        if link is None:
            pyfalog.debug('Command link is not available')
            return False
        self.savedLinkType = link.linkType
        self.savedStrength = link.strength
        self.savedMindlink = link.mindlink
        self.savedActive = link.active
        fit.commandLinks.remove(link)
        eos.db.saveddata_session.flush()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of command link {} for fit {}'.format(self.linkID, self.fitID))
        from .add import CalcAddCommandLinkCommand
        cmd = CalcAddCommandLinkCommand(
            fitID=self.fitID,
            linkType=self.savedLinkType,
            strength=self.savedStrength,
            mindlink=self.savedMindlink,
            active=self.savedActive)
        if not cmd.Do():
            return False
        # Keep our linkID in sync so a subsequent redo can find the row again
        self.linkID = cmd.savedLinkID
        return True
