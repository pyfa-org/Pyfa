import wx
from service.fit import Fit

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import InternalCommandHistory
from gui.fitCommands.calc.fitSystemSecurity import CalcChangeFitSystemSecurityCommand


class GuiChangeFitSystemSecurityCommand(wx.Command):

    def __init__(self, fitID, secStatus):
        wx.Command.__init__(self, True, 'Change Fit System Security')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.secStatus = secStatus

    def Do(self):
        cmd = CalcChangeFitSystemSecurityCommand(fitID=self.fitID, secStatus=self.secStatus)
        success = self.internalHistory.submit(cmd)
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
