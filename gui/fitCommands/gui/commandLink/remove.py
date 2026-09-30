import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandLink.remove import CalcRemoveCommandLinkCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiRemoveCommandLinksCommand(wx.Command):

    def __init__(self, fitID, linkIDs):
        wx.Command.__init__(self, True, 'Remove Command Links')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.linkIDs = linkIDs

    def Do(self):
        results = []
        for linkID in self.linkIDs:
            cmd = CalcRemoveCommandLinkCommand(fitID=self.fitID, linkID=linkID)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
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
