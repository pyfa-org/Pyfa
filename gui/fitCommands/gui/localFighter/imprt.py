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
        self.fighters = fighters

    def Do(self):
        if not self.fighters:
            return False
        commands = []
        for itemID, amount in self.fighters:
            commands.append(CalcAddLocalFighterCommand(fitID=self.fitID, fighterInfo=FighterInfo(itemID=itemID, amount=amount, state=False)))
        success = self.internalHistory.submitBatch(*commands)
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
