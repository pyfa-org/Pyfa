import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localSwap import CalcSwapLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory


class GuiSwapLocalModulesCommand(wx.Command):

    def __init__(self, fitID, position1, position2):
        wx.Command.__init__(self, True, 'Swap Local Modules')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position1 = position1
        self.position2 = position2

    def Do(self):
        if self.position1 == self.position2:
            return False
        cmd = CalcSwapLocalModuleCommand(fitID=self.fitID, position1=self.position1, position2=self.position2)
        success = self.internalHistory.submit(cmd)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
