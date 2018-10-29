import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitChangeImplantLocation import FitChangeImplantLocation


class GuiChangeImplantLocation(wx.Command):
    def __init__(self, fitID, source):
        wx.Command.__init__(self, True, "Implant Source Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.source = source

    def Do(self):
        if self.internal_history.Submit(FitChangeImplantLocation(self.fitID, self.source)):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
