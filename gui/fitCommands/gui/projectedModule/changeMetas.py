import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.projectedAdd import CalcAddProjectedModuleCommand
from gui.fitCommands.calc.module.projectedRemove import CalcRemoveProjectedModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiChangeProjectedModuleMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Projected Module Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        results = []
        for position in sorted(self.positions, reverse=True):
            module = fit.projectedModules[position]
            if module.itemID == self.newItemID:
                continue
            info = ModuleInfo.fromModule(module)
            info.itemID = self.newItemID
            cmdRemove = CalcRemoveProjectedModuleCommand(fitID=self.fitID, position=position, commit=False)
            cmdAdd = CalcAddProjectedModuleCommand(fitID=self.fitID, modInfo=info, commit=False)
            results.append(self.internalHistory.submitBatch(cmdRemove, cmdAdd))
        success = any(results)
        eos.db.commit()
        sFit.recalc(fit)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
