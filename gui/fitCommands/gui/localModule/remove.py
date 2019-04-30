import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModulesCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiRemoveLocalModuleCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.savedTypeIDs = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        self.savedTypeIDs = {m.itemID for m in fit.modules if not m.isEmpty}
        cmd = CalcRemoveLocalModulesCommand(fitID=self.fitID, positions=self.positions)
        success = self.internalHistory.submit(cmd)
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.savedTypeIDs)
            if success and self.savedTypeIDs else
            GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.savedTypeIDs)
            if success and self.savedTypeIDs else
            GE.FitChanged(fitID=self.fitID))
        return success
