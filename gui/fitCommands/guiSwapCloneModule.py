import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.module.localSwap import CalcSwapLocalModuleCommand
from .calcCommands.module.localClone import CalcCloneLocalModuleCommand
from logbook import Logger
pyfalog = Logger(__name__)


class GuiModuleSwapOrCloneCommand(wx.Command):

    def __init__(self, fitID, srcPosition, dstPosition, clone=False):
        wx.Command.__init__(self, True, "Module State Change")
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.clone = clone
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        pyfalog.debug("{} Do()".format(self))

        if self.clone:
            pyfalog.debug("Trying to clone module")
            if self.internalHistory.Submit(CalcCloneLocalModuleCommand(self.fitID, self.srcPosition, self.dstPosition)):
                Fit.getInstance().recalc(self.fitID)  # clone needs a recalc
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        else:
            pyfalog.debug("Trying to Swap module")
            if self.internalHistory.Submit(CalcSwapLocalModuleCommand(self.fitID, self.srcPosition, self.dstPosition)):
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True

        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()

        if self.clone:
            Fit.getInstance().recalc(self.fitID)

        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
