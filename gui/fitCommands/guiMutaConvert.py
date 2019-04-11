import wx

import gui.mainFrame
from gui import globalEvents as GE
from service.fit import Fit
from .calc.fitReplaceModule import FitReplaceModuleCommand


class GuiMutaConvertCommand(wx.Command):

    def __init__(self, fitID, position, mutaplasmid):
        wx.Command.__init__(self, True, "Convert Item to Mutated")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position
        self.mutaplasmid = mutaplasmid

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldMod = fit.modules[self.position]
        if oldMod.isEmpty:
            return False
        if oldMod.isMutated:
            return False

        success = self.internal_history.Submit(FitReplaceModuleCommand(
            fitID=self.fitID,
            position=self.position,
            newItemID=self.mutaplasmid.resultingItem.ID,
            newBaseItemID=oldMod.item.ID,
            newMutaplasmidID=self.mutaplasmid.ID,
            newMutations={},
            newState=oldMod.state,
            newChargeID=oldMod.chargeID))
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
