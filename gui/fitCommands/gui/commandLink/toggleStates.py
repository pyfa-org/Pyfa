import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandLink.toggleStates import CalcToggleCommandLinkStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleCommandLinkStatesCommand(wx.Command):

    def __init__(self, fitID, mainLinkID, linkIDs):
        wx.Command.__init__(self, True, 'Toggle Command Link States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainLinkID = mainLinkID
        self.linkIDs = linkIDs

    def Do(self):
        cmd = CalcToggleCommandLinkStatesCommand(
            fitID=self.fitID,
            mainLinkID=self.mainLinkID,
            linkIDs=self.linkIDs)
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
