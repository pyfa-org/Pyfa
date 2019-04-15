import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalModuleChargesCommand(wx.Command):

    def __init__(self, fitID, modules, chargeItemID):
        wx.Command.__init__(self, True, 'Change Local Module Charges')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = [mod.modPosition for mod in modules]
        self.chargeItemID = chargeItemID

    def Do(self):
        cmd = CalcChangeModuleChargesCommand(fitID=self.fitID, projected=False, chargeMap={p: self.chargeItemID for p in self.positions})
        success = self.internalHistory.submit(cmd)
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
