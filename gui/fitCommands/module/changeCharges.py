import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeModuleChargesCommand(wx.Command):

    def __init__(self, fitID, itemID, modules):
        wx.Command.__init__(self, True, 'Change Module Charges')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.positions = [mod.modPosition for mod in modules]

    def Do(self):
        cmd = CalcChangeModuleChargesCommand(fitID=self.fitID, projected=False, chargeMap={p: self.itemID for p in self.positions})
        if self.internalHistory.submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
