import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiFillWithClonedLocalModulesCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Fill with Cloned Local Modules')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.savedItemID = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        mod = fit.modules[self.position]
        self.savedItemID = mod.itemID
        info = ModuleInfo.fromModule(mod)
        added_modules = 0
        while True:
            cmd = CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=info, commit=False)
            if not self.internalHistory.submit(cmd):
                break
            added_modules += 1
        eos.db.commit()
        sFit.recalc(self.fitID)
        success = added_modules > 0
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.savedItemID)
            if success else
            GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.savedItemID)
            if success else
            GE.FitChanged(fitID=self.fitID))
        return success
