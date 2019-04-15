import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeCargoMetaCommand(wx.Command):

    def __init__(self, fitID, itemID, newItemID):
        wx.Command.__init__(self, True, 'Change Cargo Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        cargo = next((c for c in fit.cargo if c.itemID == self.itemID), None)
        if cargo is None:
            return False
        if cargo.itemID == self.newItemID:
            return False
        amount = cargo.amount
        cmdRemove = CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=math.inf))
        cmdAdd = CalcAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.newItemID, amount=amount))
        success = self.internalHistory.submitBatch(cmdRemove, cmdAdd)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
