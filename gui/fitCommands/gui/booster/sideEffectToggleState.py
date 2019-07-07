import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.booster.sideEffectToggleState import CalcToggleBoosterSideEffectStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleBoosterSideEffectStateCommand(wx.Command):

    def __init__(self, fitID, position, effectID):
        wx.Command.__init__(self, True, 'Toggle Booster Side Effect State')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.effectID = effectID

    def Do(self):
        cmd = CalcToggleBoosterSideEffectStateCommand(fitID=self.fitID, position=self.position, effectID=self.effectID)
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
