import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.booster.add import CalcAddBoosterCommand
from gui.fitCommands.helpers import BoosterInfo, InternalCommandHistory
from service.fit import Fit


class GuiSwapBoosterMetaCommand(wx.Command):

    def __init__(self, fitID, position, itemID):
        wx.Command.__init__(self, True, 'Swap Booster Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.itemID = itemID

    def Do(self):
        sFit = Fit.getInstance()
        booster = sFit.getFit(self.fitID).boosters[self.position]
        if booster.itemID == self.itemID:
            return False
        cmd = CalcAddBoosterCommand(
            fitID=self.fitID,
            boosterInfo=BoosterInfo(
                itemID=self.itemID,
                state=booster.active,
                sideEffects={se.effectID: se.active for se in booster.sideEffects}))
        if self.internalHistory.submit(cmd):
            sFit.recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
