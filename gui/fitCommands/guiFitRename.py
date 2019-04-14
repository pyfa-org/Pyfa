import wx
import gui.mainFrame
from .calcCommands.fitRename import CalcFitRenameCommand
from service.fit import Fit
from logbook import Logger
from gui.builtinShipBrowser.events import FitRenamed
pyfalog = Logger(__name__)


class GuiFitRenameCommand(wx.Command):
    def __init__(self, fitID, newName):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newName = newName
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        if self.internalHistory.Submit(CalcFitRenameCommand(self.fitID, self.newName)):
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), FitRenamed(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), FitRenamed(fitID=self.fitID))
        return True
