import math
import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeCargoMetasCommand(wx.Command):

    def __init__(self, fitID, itemIDs, newItemID):
        wx.Command.__init__(self, True, 'Change Cargo Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemIDs = itemIDs
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        results = []
        for itemID in self.itemIDs:
            if itemID == self.newItemID:
                continue
            cargo = next((c for c in fit.cargo if c.itemID == itemID), None)
            if cargo is None:
                continue
            amount = cargo.amount
            cmdRemove = CalcRemoveCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=itemID, amount=math.inf))
            cmdAdd = CalcAddCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=self.newItemID, amount=amount))
            results.append(self.internalHistory.submitBatch(cmdRemove, cmdAdd))
        success = any(results)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
