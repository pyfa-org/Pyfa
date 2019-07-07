import math

import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedChangeAmount import CalcChangeProjectedDroneAmountCommand
from gui.fitCommands.calc.drone.projectedRemove import CalcRemoveProjectedDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedDroneAmountCommand(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Change Projected Drone Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeProjectedDroneAmountCommand(fitID=self.fitID, itemID=self.itemID, amount=self.amount)
        else:
            cmd = CalcRemoveProjectedDroneCommand(fitID=self.fitID, itemID=self.itemID, amount=math.inf)
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
