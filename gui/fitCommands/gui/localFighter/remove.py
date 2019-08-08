import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.localRemove import CalcRemoveLocalFighterCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit
from service.market import Market


class GuiRemoveLocalFightersCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Local Fighters')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions

    def Do(self):
        sMkt = Market.getInstance()
        results = []
        for position in sorted(self.positions, reverse=True):
            cmd = CalcRemoveLocalFighterCommand(fitID=self.fitID, position=position)
            results.append(self.internalHistory.submit(cmd))
            sMkt.storeRecentlyUsed(cmd.savedFighterInfo.itemID)
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
