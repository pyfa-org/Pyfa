import wx

import gui.mainFrame
from eos.saveddata.drone import Drone as DroneType
from eos.saveddata.fighter import Fighter as FighterType
from eos.saveddata.fit import Fit as FitType
from eos.saveddata.module import Module as ModuleType
from gui import globalEvents as GE
from service.fit import Fit
from .calc.fitToggleProjectedDrone import FitToggleProjectedDroneCommand
from .calc.fitToggleProjectedFighter import FitToggleProjectedFighterCommand
from .calc.fitToggleProjectedFit import FitToggleProjectedFitCommand
from .calc.fitToggleProjectedModule import FitToggleProjectedModuleCommand


class GuiToggleProjectedCommand(wx.Command):

    def __init__(self, fitID, thing, click):
        wx.Command.__init__(self, True, "Toggle Projected Item")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.thing = thing
        self.click = click

    def Do(self):
        fit = Fit.getInstance().getFit(self.fitID)
        if isinstance(self.thing, FitType):
            success = self.internal_history.Submit(FitToggleProjectedFitCommand(self.fitID, self.thing.ID))
        elif isinstance(self.thing, ModuleType):
            position = fit.projectedModules.index(self.thing)
            success = self.internal_history.Submit(FitToggleProjectedModuleCommand(self.fitID, position, self.click))
        elif isinstance(self.thing, DroneType):
            position = fit.projectedDrones.index(self.thing)
            success = self.internal_history.Submit(FitToggleProjectedDroneCommand(self.fitID, position))
        elif isinstance(self.thing, FighterType):
            position = fit.projectedFighters.index(self.thing)
            success = self.internal_history.Submit(FitToggleProjectedFighterCommand(self.fitID, position))
        else:
            success = False
        if not success:
            return False
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True


    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
