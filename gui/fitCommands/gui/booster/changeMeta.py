import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.booster.add import CalcAddBoosterCommand
from gui.fitCommands.helpers import BoosterInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeBoosterMetaCommand(wx.Command):

    def __init__(self, fitID, position, newItemID):
        wx.Command.__init__(self, True, 'Change Booster Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        booster = fit.boosters[self.position]
        if booster.itemID == self.newItemID:
            return False
        info = BoosterInfo.fromBooster(booster)
        info.itemID = self.newItemID
        cmd = CalcAddBoosterCommand(fitID=self.fitID, boosterInfo=info)
        success = self.internalHistory.submit(cmd)
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
