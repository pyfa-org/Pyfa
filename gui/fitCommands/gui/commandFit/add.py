import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.commandFit.add import CalcAddCommandCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiAddCommandFitCommand(wx.Command):

    def __init__(self, fitID, commandFitID):
        wx.Command.__init__(self, True, 'Add Command Fit')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.commandFitID = commandFitID

    def Do(self):
        cmd = CalcAddCommandCommand(fitID=self.fitID, commandFitID=self.commandFitID)
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
