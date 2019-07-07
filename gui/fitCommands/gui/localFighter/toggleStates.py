import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fighter.localToggleStates import CalcToggleLocalFighterStatesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiToggleLocalFighterStatesCommand(wx.Command):

    def __init__(self, fitID, mainPosition, positions):
        wx.Command.__init__(self, True, 'Toggle Local Fighter States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.mainPosition = mainPosition
        self.positions = positions

    def Do(self):
        cmd = CalcToggleLocalFighterStatesCommand(
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
