import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo
from service.fit import Fit
from .calcCommands.module.localReplace import CalcReplaceLocalModuleCommand


class GuiMutaRevertCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Convert Item to Normal")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldMod = fit.modules[self.position]
        if oldMod.isEmpty:
            return False
        if not oldMod.isMutated:
            return False

        success = self.internalHistory.Submit(CalcReplaceLocalModuleCommand(
            fitID=self.fitID,
            position=self.position,
            newModInfo=ModuleInfo(
                itemID=oldMod.baseItemID,
                chargeID=oldMod.chargeID,
                state=oldMod.state,
                spoolType=oldMod.spoolType,
                spoolAmount=oldMod.spoolAmount)))
        if not success:
            return False

        sFit.recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
