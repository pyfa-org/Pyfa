import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.booster.add import CalcAddBoosterCommand
from gui.fitCommands.helpers import BoosterInfo, InternalCommandHistory
from service.fit import Fit


class GuiImportBoostersCommand(wx.Command):

    def __init__(self, fitID, boosters):
        wx.Command.__init__(self, True, 'Import Boosters')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.boosters = set(b[0] for b in boosters)

    def Do(self):
        results = []
        for itemID in self.boosters:
            cmd = CalcAddBoosterCommand(fitID=self.fitID, boosterInfo=BoosterInfo(itemID=itemID))
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
