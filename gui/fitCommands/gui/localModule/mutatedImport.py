import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiImportLocalMutatedModuleCommand(wx.Command):

    def __init__(self, fitID, baseItem, mutaplasmid, mutations):
        wx.Command.__init__(self, True, 'Import Local Mutated Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.newModInfo = ModuleInfo(
            itemID=mutaplasmid.resultingItem.ID,
            baseItemID=baseItem.ID,
            mutaplasmidID=mutaplasmid.ID,
            mutations=mutations)

    def Do(self):
        cmd = CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=self.newModInfo)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.newModInfo.itemID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.newModInfo.itemID))
        return success
