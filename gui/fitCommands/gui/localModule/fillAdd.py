import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit
from service.market import Market


class GuiFillWithNewLocalModulesCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Fill with New Local Modules')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.savedRemovedDummies = None

    def Do(self):
        info = ModuleInfo(itemID=self.itemID)
        added_modules = 0
        while True:
            cmd = CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=info)
            if not self.internalHistory.submit(cmd):
                break
            added_modules += 1
        Market.getInstance().storeRecentlyUsed(self.itemID)
        sFit = Fit.getInstance()
        # Only last command decides if we need to recalc here or not
        if cmd.needsGuiRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        success = added_modules > 0
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.itemID)
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
            GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.itemID)
            if success else
            GE.FitChanged(fitIDs=(self.fitID,)))
        return success
