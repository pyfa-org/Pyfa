import wx
import gui.mainFrame
from .calc.fitRename import FitRenameCommand
from service.fit import Fit
from logbook import Logger
from gui.builtinShipBrowser.events import FitRenamed
pyfalog = Logger(__name__)


class GuiFitRenameCommand(wx.Command):
    def __init__(self, fitID, newName):
        wx.Command.__init__(self, True)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.newName = newName
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        if self.internal_history.Submit(FitRenameCommand(self.fitID, self.newName)):
            wx.PostEvent(self.mainFrame, FitRenamed(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, FitRenamed(fitID=self.fitID))
        return True
