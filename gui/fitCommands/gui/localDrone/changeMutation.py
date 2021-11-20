import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.localChangeMutation import CalcChangeLocalDroneMutationCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalDroneMutationCommand(wx.Command):

    def __init__(self, fitID, position, mutation, oldMutation=None):
        wx.Command.__init__(self, True, 'Change Local Drone Mutation')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.mutation = mutation
        self.oldMutation = oldMutation

    def Do(self):
        cmd = CalcChangeLocalDroneMutationCommand(
            fitID=self.fitID,
            position=self.position,
            mutation=self.mutation,
            oldMutation=self.oldMutation)
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
