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
        self.newPosition = None

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
        self.newPosition = cmd.newPosition
        newBooster = fit.boosters[self.newPosition]
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        wx.PostEvent(mainFrame, GE.FitChanged(fitIDs=(self.fitID,)))
        wx.PostEvent(mainFrame, GE.ItemChangedInplace(old=booster, new=newBooster))
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldBooster = fit.boosters[self.newPosition]
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        newBooster = fit.boosters[self.position]
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        wx.PostEvent(mainFrame, GE.FitChanged(fitIDs=(self.fitID,)))
        wx.PostEvent(mainFrame, GE.ItemChangedInplace(old=oldBooster, new=newBooster))
        return success
