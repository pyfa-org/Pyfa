import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiRevertMutatedModuleCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Revert Module from Mutated')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        mod = fit.modules[self.position]
        if mod.isEmpty:
            return False
        if not mod.isMutated:
            return False
        cmd = CalcReplaceLocalModuleCommand(
            fitID=self.fitID,
            position=self.position,
            newModInfo=ModuleInfo(
                itemID=mod.baseItemID,
                chargeID=mod.chargeID,
                state=mod.state,
                spoolType=mod.spoolType,
                spoolAmount=mod.spoolAmount))
        if self.internalHistory.submit(cmd):
            sFit.recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
