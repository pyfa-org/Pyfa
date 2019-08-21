import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.helpers import DroneInfo, InternalCommandHistory
from service.fit import Fit


class GuiImportLocalDronesCommand(wx.Command):

    def __init__(self, fitID, drones):
        wx.Command.__init__(self, True, 'Import Local Drones')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.drones = drones

    def Do(self):
        if not self.drones:
            return False
        commands = []
        for itemID, amount in self.drones:
            commands.append(CalcAddLocalDroneCommand(
                fitID=self.fitID,
                droneInfo=DroneInfo(itemID=itemID, amount=amount, amountActive=0),
                forceNewStack=True))
        success = self.internalHistory.submitBatch(*commands)
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
