import wx

import gui.mainFrame
from gui.builtinShipBrowser.events import FitRenamed
from gui.fitCommands.calcCommands.fitRename import CalcFitRenameCommand
from gui.fitCommands.helpers import InternalCommandHistory


class GuiRenameFitCommand(wx.Command):

    def __init__(self, fitID, name):
        wx.Command.__init__(self, True, 'Rename Fit')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.name = name

    def Do(self):
        cmd = CalcFitRenameCommand(fitID=self.fitID, name=self.name)
        if self.internalHistory.submit(cmd):
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), FitRenamed(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), FitRenamed(fitID=self.fitID))
        return success
