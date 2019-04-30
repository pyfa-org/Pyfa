import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiReplaceLocalModuleCommand(wx.Command):

    def __init__(self, fitID, itemID, positions):
        wx.Command.__init__(self, True, 'Replace Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.positions = positions
        self.savedRemovedDummies = None

    def Do(self):
        results = []
        for position in self.positions:
            cmd = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=position,
                newModInfo=ModuleInfo(itemID=self.itemID),
                commit=False)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
        eos.db.commit()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.itemID)
            if success else
            GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        eos.db.commit()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.itemID)
            if success else
            GE.FitChanged(fitID=self.fitID))
        return success
