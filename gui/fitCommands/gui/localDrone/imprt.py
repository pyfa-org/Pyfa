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
        self.droneInfos = []
        for itemID, amount, mutation in drones:
            if mutation:
                mutaplasmid, attrs = mutation
                self.droneInfos.append(DroneInfo(
                    itemID=mutaplasmid.resultingItem.ID,
                    amount=amount,
                    amountActive=0,
                    baseItemID=itemID,
                    mutaplasmidID=mutaplasmid.ID,
                    mutations=attrs))
            else:
                self.droneInfos.append(DroneInfo(itemID=itemID, amount=amount, amountActive=0))

    def Do(self):
        results = []
        for info in self.droneInfos:
            cmd = CalcAddLocalDroneCommand(fitID=self.fitID, droneInfo=info, forceNewStack=True)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
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
