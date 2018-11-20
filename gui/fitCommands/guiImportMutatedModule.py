import wx
import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitImportMutatedModule import FitImportMutatedCommand
from service.fit import Fit
from logbook import Logger
pyfalog = Logger(__name__)


class GuiImportMutatedModuleCommand(wx.Command):

    def __init__(self, fitID, baseItem, mutaItem, attrMap):
        wx.Command.__init__(self, True, "Mutated Module Import: {} {} {}".format(baseItem, mutaItem, attrMap))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.baseItem = baseItem
        self.mutaItem = mutaItem
        self.attrMap = attrMap
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        pyfalog.debug("{} Do()".format(self))

        if self.internal_history.Submit(FitImportMutatedCommand(self.fitID, self.baseItem, self.mutaItem, self.attrMap)):
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
