import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiConvertMutatedLocalModuleCommand(wx.Command):

    def __init__(self, fitID, position, mutaplasmid):
        wx.Command.__init__(self, True, 'Convert Local Module to Mutated')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.itemID = mutaplasmid.resultingItem.ID
        self.mutaplasmidID = mutaplasmid.ID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        mod = fit.modules[self.position]
        if mod.isEmpty:
            return False
        if mod.isMutated:
            return False
        cmd = CalcReplaceLocalModuleCommand(
            fitID=self.fitID,
            position=self.position,
            newModInfo=ModuleInfo(
                itemID=self.itemID,
                baseItemID=mod.item.ID,
                mutaplasmidID=self.mutaplasmidID,
                mutations={},
                chargeID=mod.chargeID,
                state=mod.state,
                spoolType=mod.spoolType,
                spoolAmount=mod.spoolAmount))
        success = self.internalHistory.submit(cmd)
        sFit.recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
