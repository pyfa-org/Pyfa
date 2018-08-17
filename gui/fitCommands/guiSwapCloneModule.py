import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fitSwapModule import FitSwapModuleCommand
from .calc.fitCloneModule import FitCloneModuleCommand
from logbook import Logger
pyfalog = Logger(__name__)


class GuiModuleSwapOrCloneCommand(wx.Command):

    def __init__(self, fitID, srcPosition, dstPosition, clone=False):
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.clone = clone
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        pyfalog.debug("{} Do()".format(self))

        if self.clone:
            pyfalog.debug("Trying to clone module")
            if self.internal_history.Submit(FitCloneModuleCommand(self.fitID, self.srcPosition, self.dstPosition)):
                self.sFit.recalc(self.fitID)  # clone needs a recalc
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
                return True
        else:
            pyfalog.debug("Trying to Swap module")
            if self.internal_history.Submit(FitSwapModuleCommand(self.fitID, self.srcPosition, self.dstPosition)):
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
                return True

        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()

        if self.clone:
            self.sFit.recalc(self.fitID)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
