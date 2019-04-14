import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.cargo.changeAmount import CalcChangeCargoAmountCommand
from gui.fitCommands.calcCommands.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory


class GuiChangeCargoAmount(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Change Cargo Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            if self.internalHistory.submit(CalcChangeCargoAmountCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=self.amount))):
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        else:
            if self.internalHistory.submit(CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=math.inf))):
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
