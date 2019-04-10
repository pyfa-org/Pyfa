import wx

import eos.db
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
        fit = eos.db.getFit(self.fitID)
        oldMod = fit.modules[self.position]

        success = self.internal_history.Submit(FitReplaceModuleCommand(
            fitID=self.fitID,
            position=self.position,
            newItemID=self.mutaplasmid.resultingItem.ID,
            newBaseItemID=oldMod.item.ID,
            newMutaplasmidID=self.mutaplasmid.ID,
            newMutations={},
            newState=oldMod.state,
            newCharge=oldMod.charge))
        if not success:
            return False

        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
