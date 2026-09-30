import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandLink.add import CalcAddCommandLinkCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiAddCommandLinkCommand(wx.Command):

    def __init__(self, fitID, linkType, strength, mindlink):
        wx.Command.__init__(self, True, 'Add Command Link')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.linkType = linkType
        self.strength = strength
        self.mindlink = mindlink

    def Do(self):
        cmd = CalcAddCommandLinkCommand(
            fitID=self.fitID,
            linkType=self.linkType,
            strength=self.strength,
            mindlink=self.mindlink)
        success = self.internalHistory.submit(cmd)
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
