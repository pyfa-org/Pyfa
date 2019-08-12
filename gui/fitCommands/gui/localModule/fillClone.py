import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiFillWithClonedLocalModulesCommand(wx.Command):

    def __init__(self, fitID, position):
        wx.Command.__init__(self, True, 'Fill with Cloned Local Modules')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.savedItemID = None
        self.savedRemovedDummies = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        mod = fit.modules[self.position]
        self.savedItemID = mod.itemID
        info = ModuleInfo.fromModule(mod)
        added_modules = 0
        while True:
            cmd = CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=info)
            if not self.internalHistory.submit(cmd):
                break
            added_modules += 1
        if cmd.needsGuiRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        success = added_modules > 0
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.savedItemID)
            if success else
            GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.savedItemID)
            if success else
            GE.FitChanged(fitIDs=(self.fitID,)))
        return success
