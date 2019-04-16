import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.projectedAdd import CalcAddProjectedModuleCommand
from gui.fitCommands.calc.module.projectedRemove import CalcRemoveProjectedModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiChangeProjectedModuleMetaCommand(wx.Command):

    def __init__(self, fitID, position, newItemID):
        wx.Command.__init__(self, True, 'Change Projected Module Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        module = fit.projectedModules[self.position]
        if module.itemID == self.newItemID:
            return
        info = ModuleInfo.fromModule(module)
        info.itemID = self.newItemID
        cmdRemove = CalcRemoveProjectedModuleCommand(fitID=self.fitID, position=self.position)
        cmdAdd = CalcAddProjectedModuleCommand(fitID=self.fitID, modInfo=info)
        success = self.internalHistory.submitBatch(cmdRemove, cmdAdd)
        sFit.recalc(fit)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
