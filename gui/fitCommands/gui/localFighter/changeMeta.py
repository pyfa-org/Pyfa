import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.localAdd import CalcAddLocalFighterCommand
from gui.fitCommands.calc.fighter.localRemove import CalcRemoveLocalFighterCommand
from gui.fitCommands.helpers import FighterInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalFighterMetaCommand(wx.Command):

    def __init__(self, fitID, position, newItemID):
        wx.Command.__init__(self, True, 'Change Local Fighter Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        fighter = fit.fighters[self.position]
        if fighter.itemID == self.newItemID:
            return False
        info = FighterInfo.fromFighter(fighter)
        info.itemID = self.newItemID
        cmdRemove = CalcRemoveLocalFighterCommand(fitID=self.fitID, position=self.position)
        cmdAdd = CalcAddLocalFighterCommand(fitID=self.fitID, fighterInfo=info)
        success = self.internalHistory.submitBatch(cmdRemove, cmdAdd)
        sFit.recalc(fit)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
