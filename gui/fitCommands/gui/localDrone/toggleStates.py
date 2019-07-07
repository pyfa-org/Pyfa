import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localToggleStates import CalcToggleLocalDroneStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleLocalDroneStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions):
        wx.Command.__init__(self, True, 'Toggle Local Drone States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions

    def Do(self):
        cmd = CalcToggleLocalDroneStatesCommand(
            fitID=self.fitID,
            mainPosition=self.mainPosition,
            positions=self.positions)
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
