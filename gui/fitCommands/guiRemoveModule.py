import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .helpers import ModuleInfo
from .calc.fitRemoveModule import FitRemoveModuleCommand


class GuiModuleRemoveCommand(wx.Command):
    def __init__(self, fitID, modules):
        """
        Handles removing modules from fit.modules,

        :param fitID: The fit ID that we are modifying
        :param modules: A list of Module objects that we are attempting to remove.
        """
        wx.Command.__init__(self, True, "Module Remove")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.modCache = {mod.modPosition: ModuleInfo.fromModule(mod) for mod in modules if not mod.isEmpty}
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        success = self.internal_history.Submit(FitRemoveModuleCommand(self.fitID, [pos for pos in self.modCache]))

        if success:
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=set([mod.itemID for mod in self.modCache.values()])))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=set([mod.itemID for mod in self.modCache.values()])))
        return True
