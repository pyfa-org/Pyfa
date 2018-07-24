import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from collections import namedtuple

from .helpers import ModuleInfoCache
from .fitRemoveModule import FitRemoveModuleCommand


class GuiModuleRemoveCommand(wx.Command):
    def __init__(self, fitID, modules):
        # todo: evaluate mutaplasmid modules
        wx.Command.__init__(self, True, "Module Remove")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.modCache = [ModuleInfoCache(mod.modPosition, mod.item.ID, mod.state, mod.charge) for mod in modules]
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        # todo: what happens when one remove in an array of removes fucks up? (it really shouldn't it's easy peasy)
        success = self.internal_history.Submit(FitRemoveModuleCommand(self.fitID, [mod.modPosition for mod in self.modCache]))

        if success is not None:
            # self.slotsChanged() # todo: fix
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=set([mod.itemID for mod in self.modCache])))
            return True

    def Undo(self):
        for x in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=set([mod.itemID for mod in self.modCache])))
        return True
