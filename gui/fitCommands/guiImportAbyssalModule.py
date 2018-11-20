import wx
import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitImportAbyssalModule import FitImportAbyssalCommand
from service.fit import Fit
from logbook import Logger
pyfalog = Logger(__name__)


class GuiImportAbyssalModuleCommand(wx.Command):
    def __init__(self, fitID, module):
        wx.Command.__init__(self, True, "Abyssal Module Import: {}".format(module))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.module = module
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        pyfalog.debug("{} Do()".format(self))

        if self.internal_history.Submit(FitImportAbyssalCommand(self.fitID, self.module)):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd"))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel"))
        return True
