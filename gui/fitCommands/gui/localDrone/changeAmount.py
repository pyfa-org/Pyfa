import math

import wx

import eos.db
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
        else:
            cmd = CalcRemoveLocalDroneCommand(fitID=self.fitID, position=self.position, amount=math.inf)
        success = self.internalHistory.submit(cmd)
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
