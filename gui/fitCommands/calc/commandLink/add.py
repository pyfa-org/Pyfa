import wx
from logbook import Logger

import eos.db
from eos.saveddata.commandLink import CommandLink
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddCommandLinkCommand(wx.Command):

    def __init__(self, fitID, linkType, strength, mindlink, active=True):
        wx.Command.__init__(self, True, 'Add Command Link')
        self.fitID = fitID
        self.linkType = linkType
        self.strength = strength
        self.mindlink = mindlink
        self.active = active
        self.savedLinkID = None

    def Do(self):
        pyfalog.debug('Doing addition of command link {} for fit {}'.format(self.linkType, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        if fit is None:
            return False
        link = CommandLink(self.linkType, self.strength, self.mindlink, self.active)
        fit.commandLinks.append(link)
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(link)
        self.savedLinkID = link.ID
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of command link {} for fit {}'.format(self.linkType, self.fitID))
        from .remove import CalcRemoveCommandLinkCommand
        cmd = CalcRemoveCommandLinkCommand(fitID=self.fitID, linkID=self.savedLinkID)
        return cmd.Do()
