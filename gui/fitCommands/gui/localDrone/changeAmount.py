import math

import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localChangeAmount import CalcChangeLocalDroneAmountCommand
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalDroneAmountCommand(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Change Local Drone Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeLocalDroneAmountCommand(fitID=self.fitID, position=self.position, amount=self.amount)
            if self.internalHistory.submit(cmd):
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        else:
            cmd = CalcRemoveLocalDroneCommand(fitID=self.fitID, position=self.position, amount=math.inf)
            if self.internalHistory.submit(cmd):
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
