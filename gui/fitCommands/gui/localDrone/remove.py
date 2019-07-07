import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localRemove import CalcRemoveLocalDroneCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiRemoveLocalDronesCommand(wx.Command):

    def __init__(self, fitID, positions, amount):
        wx.Command.__init__(self, True, 'Remove Local Drones')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.amount = amount

    def Do(self):
        results = []
        for position in sorted(self.positions, reverse=True):
            cmd = CalcRemoveLocalDroneCommand(
                fitID=self.fitID,
                position=position,
                amount=self.amount)
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
