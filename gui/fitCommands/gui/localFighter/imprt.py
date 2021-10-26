import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.localAdd import CalcAddLocalFighterCommand
from gui.fitCommands.helpers import FighterInfo, InternalCommandHistory
from service.fit import Fit


class GuiImportLocalFightersCommand(wx.Command):

    def __init__(self, fitID, fighters):
        wx.Command.__init__(self, True, 'Import Local Fighters')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.fighters = [(i, a) for i, a, m in fighters]

    def Do(self):
        results = []
        for itemID, amount in self.fighters:
            cmd = CalcAddLocalFighterCommand(fitID=self.fitID, fighterInfo=FighterInfo(itemID=itemID, amount=amount, state=False))
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
