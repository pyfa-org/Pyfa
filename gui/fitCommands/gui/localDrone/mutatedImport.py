import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localAdd import CalcAddLocalDroneCommand
from gui.fitCommands.helpers import InternalCommandHistory, DroneInfo
from service.fit import Fit


class GuiImportLocalMutatedDroneCommand(wx.Command):

    def __init__(self, fitID, baseItem, mutaplasmid, mutations, amount):
        wx.Command.__init__(self, True, 'Import Local Mutated Drone')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.newDroneInfo = DroneInfo(
            amount=amount,
            amountActive=0,
            itemID=mutaplasmid.resultingItem.ID,
            baseItemID=baseItem.ID,
            mutaplasmidID=mutaplasmid.ID,
            mutations=mutations)

    def Do(self):
        cmd = CalcAddLocalDroneCommand(fitID=self.fitID, droneInfo=self.newDroneInfo, forceNewStack=True)
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
