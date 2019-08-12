import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModulesCommand
from gui.fitCommands.helpers import InternalCommandHistory, restoreRemovedDummies
from service.fit import Fit
from service.market import Market


class GuiRemoveLocalModuleCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.savedTypeIDs = None
        self.savedRemovedDummies = None

    def Do(self):
        sMkt = Market.getInstance()
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        self.savedTypeIDs = {m.itemID for m in fit.modules if not m.isEmpty}
        cmd = CalcRemoveLocalModulesCommand(fitID=self.fitID, positions=self.positions)
        success = self.internalHistory.submit(cmd)
        for container in (cmd.savedSubInfos, cmd.savedModInfos):
            for position in sorted(container, reverse=True):
                modInfo = container[position]
                sMkt.storeRecentlyUsed(modInfo.itemID)
        if cmd.needsGuiRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.savedTypeIDs)
            if success and self.savedTypeIDs else
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
            GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.savedTypeIDs)
            if success and self.savedTypeIDs else
            GE.FitChanged(fitIDs=(self.fitID,)))
        return success
