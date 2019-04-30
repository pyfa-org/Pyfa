import wx
from service.fit import Fit

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import InternalCommandHistory
from gui.fitCommands.calc.implant.remove import CalcRemoveImplantCommand


class GuiRemoveImplantsCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Implants')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions

    def Do(self):
        results = []
        for position in sorted(self.positions, reverse=True):
            cmd = CalcRemoveImplantCommand(fitID=self.fitID, position=position, commit=False)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
        eos.db.commit()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
