import wx
from logbook import Logger

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo
from service.fit import Fit
from .calc.module.localAdd import CalcAddLocalModuleCommand


pyfalog = Logger(__name__)


class GuiImportMutatedModuleCommand(wx.Command):

    def __init__(self, fitID, baseItem, mutaplasmid, mutations):
        wx.Command.__init__(self, True, "Mutated Module Import: {} {} {}".format(baseItem, mutaplasmid, mutations))
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.newModInfo = ModuleInfo(
            itemID=mutaplasmid.resultingItem.ID,
            baseItemID=baseItem.ID,
            mutaplasmidID=mutaplasmid.ID,
            mutations=mutations)

    def Do(self):
        pyfalog.debug("{} Do()".format(self))

        if self.internalHistory.Submit(CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=self.newModInfo)):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action="modadd"))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action="moddel"))
        return True
