import wx
from service.fit import Fit

import gui.mainFrame
from eos.const import ImplantLocation
from gui import globalEvents as GE
from gui.fitCommands.helpers import ImplantInfo
from .calc.fitAddImplant import FitAddImplantCommand
from .calc.fitChangeImplantLocation import FitChangeImplantLocationCommand


class GuiAddImplantCommand(wx.Command):
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Implant Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        if (
            self.internal_history.Submit(FitAddImplantCommand(fitID=self.fitID, implantInfo=ImplantInfo(itemID=self.itemID))) and
            self.internal_history.Submit(FitChangeImplantLocationCommand(self.fitID, ImplantLocation.FIT))
        ):
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
