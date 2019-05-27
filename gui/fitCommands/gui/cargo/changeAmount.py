import math

import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.changeAmount import CalcChangeCargoAmountCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory


class GuiChangeCargoAmountCommand(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Change Cargo Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeCargoAmountCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=self.amount))
        else:
            cmd = CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=math.inf))
        success = self.internalHistory.submit(cmd)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
