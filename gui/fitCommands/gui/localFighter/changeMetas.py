import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.localAdd import CalcAddLocalFighterCommand
from gui.fitCommands.calc.fighter.localRemove import CalcRemoveLocalFighterCommand
from gui.fitCommands.helpers import FighterInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalFighterMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Local Fighter Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        results = []
        for position in sorted(self.positions, reverse=True):
            fighter = fit.fighters[position]
            if fighter.itemID == self.newItemID:
                continue
            info = FighterInfo.fromFighter(fighter)
            info.itemID = self.newItemID
            cmdRemove = CalcRemoveLocalFighterCommand(
                fitID=self.fitID,
                position=position)
            cmdAdd = CalcAddLocalFighterCommand(
                fitID=self.fitID,
                fighterInfo=info,
                ignoreRestrictions=True)
            results.append(self.internalHistory.submitBatch(cmdRemove, cmdAdd))
        success = any(results)
        eos.db.flush()
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
