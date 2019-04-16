import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiChangeLocalModuleMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Local Module Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        commands = []
        for position in self.positions:
            module = fit.modules[position]
            if module.itemID == self.newItemID:
                continue
            info = ModuleInfo.fromModule(module)
            info.itemID = self.newItemID
            cmd = CalcReplaceLocalModuleCommand(fitID=self.fitID, position=position, newModInfo=info, unloadInvalidCharges=True, commit=False)
            commands.append(cmd)
        if not commands:
            return False
        success = self.internalHistory.submitBatch(*commands)
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
