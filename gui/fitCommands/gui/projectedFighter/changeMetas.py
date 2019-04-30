import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.projectedAdd import CalcAddProjectedFighterCommand
from gui.fitCommands.calc.fighter.projectedRemove import CalcRemoveProjectedFighterCommand
from gui.fitCommands.helpers import FighterInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedFighterMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Projected Fighter Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        results = []
        for position in sorted(self.positions, reverse=True):
            fighter = fit.projectedFighters[position]
            if fighter.itemID == self.newItemID:
                continue
            info = FighterInfo.fromFighter(fighter)
            info.itemID = self.newItemID
            cmdRemove = CalcRemoveProjectedFighterCommand(fitID=self.fitID, position=position, commit=False)
            cmdAdd = CalcAddProjectedFighterCommand(fitID=self.fitID, fighterInfo=info, commit=False)
            results.append(self.internalHistory.submitBatch(cmdRemove, cmdAdd))
        success = any(results)
        eos.db.commit()
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
