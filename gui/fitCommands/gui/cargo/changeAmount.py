import math

import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.changeAmount import CalcChangeCargoAmountCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory


class GuiChangeCargosAmountCommand(wx.Command):

    def __init__(self, fitID, itemIDs, amount):
        wx.Command.__init__(self, True, 'Change Cargo Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemIDs = itemIDs
        self.amount = amount

    def Do(self):
        results = []
        if self.amount > 0:
            for itemID in self.itemIDs:
                cmd = CalcChangeCargoAmountCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=itemID, amount=self.amount))
                results.append(self.internalHistory.submit(cmd))
        else:
            for itemID in self.itemIDs:
                cmd = CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=itemID, amount=math.inf))
                results.append(self.internalHistory.submit(cmd))
        success = any(results)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
