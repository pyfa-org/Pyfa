import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.changeAmount import CalcChangeFighterAmountCommand
from gui.fitCommands.calc.fighter.projectedRemove import CalcRemoveProjectedFighterCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedFighterAmountCommand(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Change Projected Fighter Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeFighterAmountCommand(fitID=self.fitID, projected=True, position=self.position, amount=self.amount)
        else:
            cmd = CalcRemoveProjectedFighterCommand(fitID=self.fitID, position=self.position)
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
