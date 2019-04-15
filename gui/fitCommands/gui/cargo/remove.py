import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory


class GuiRemoveCargoCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Remove Cargo')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        cmd = CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.itemID, amount=math.inf))
        if self.internalHistory.submit(cmd):
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
