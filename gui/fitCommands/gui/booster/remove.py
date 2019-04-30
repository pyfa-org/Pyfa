import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.booster.remove import CalcRemoveBoosterCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiRemoveBoostersCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Boosters')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions

    def Do(self):
        results = []
        for position in sorted(self.positions, reverse=True):
            cmd = CalcRemoveBoosterCommand(fitID=self.fitID, position=position, commit=False)
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
