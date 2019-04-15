import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.module.localRemove import CalcRemoveLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiRemoveLocalModuleCommand(wx.Command):

    def __init__(self, fitID, modules):
        wx.Command.__init__(self, True, 'Remove Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.modCache = {mod.modPosition: ModuleInfo.fromModule(mod) for mod in modules if not mod.isEmpty}

    def Do(self):
        cmd = CalcRemoveLocalModuleCommand(fitID=self.fitID, positions=[pos for pos in self.modCache])
        if self.internalHistory.submit(cmd):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(
                gui.mainFrame.MainFrame.getInstance(),
                GE.FitChanged(fitID=self.fitID, action='moddel', typeID=set([mod.itemID for mod in self.modCache.values()])))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=set([mod.itemID for mod in self.modCache.values()])))
        return success
