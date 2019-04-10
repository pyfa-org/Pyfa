import wx

import gui.mainFrame
from gui import globalEvents as GE
from service.fit import Fit
from .calc.fitReplaceModule import FitReplaceModuleCommand


class GuiMutaRevertCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, "Convert Item to Normal")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.internal_history = wx.CommandProcessor()
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

        success = self.internal_history.Submit(FitReplaceModuleCommand(
            fitID=self.fitID,
            position=self.position,
            newItemID=oldMod.baseItemID,
            newBaseItemID=None,
            newMutaplasmidID=None,
            newMutations=None,
            newState=oldMod.state,
            newCharge=oldMod.charge))
        if not success:
            return False

        sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
