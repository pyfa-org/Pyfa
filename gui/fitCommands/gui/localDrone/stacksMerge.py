import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localChangeAmount import CalcChangeLocalDroneAmountCommand
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiMergeLocalDroneStacksCommand(wx.Command):

    def __init__(self, fitID, srcPosition, dstPosition):
        wx.Command.__init__(self, True, 'Merge Local Drone Stacks')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition

    def Do(self):
        if self.srcPosition == self.dstPosition:
            return False
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        srcDrone = fit.drones[self.srcPosition]
        dstDrone = fit.drones[self.dstPosition]
        if srcDrone.itemID != dstDrone.itemID:
            return False
        srcAmount = srcDrone.amount
        commands = []
        commands.append(CalcChangeLocalDroneAmountCommand(
            fitID=self.fitID,
            position=self.dstPosition,
            amount=dstDrone.amount + srcAmount))
        commands.append(CalcRemoveLocalDroneCommand(
            fitID=self.fitID,
            position=self.srcPosition,
            amount=srcAmount))
        success = self.internalHistory.submitBatch(*commands)
        eos.db.flush()
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
