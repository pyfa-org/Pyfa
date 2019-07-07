import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandFit.remove import CalcRemoveCommandFitCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiRemoveCommandFitsCommand(wx.Command):

    def __init__(self, fitID, commandFitIDs):
        wx.Command.__init__(self, True, 'Remove Command Fits')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.commandFitIDs = commandFitIDs

    def Do(self):
        results = []
        for commandFitID in self.commandFitIDs:
            cmd = CalcRemoveCommandFitCommand(fitID=self.fitID, commandFitID=commandFitID)
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
