import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.module.projectedRemove import FitRemoveProjectedModuleCommand
from .calc.projectedFit.remove import FitRemoveProjectedFitCommand
from .calc.fighter.projectedRemove import FitRemoveProjectedFighterCommand
from logbook import Logger
from .calc.drone.projectedRemove import FitRemoveProjectedDroneCommand

from gui.fitCommands.helpers import DroneInfo
from eos.saveddata.drone import Drone
from eos.saveddata.module import Module
from eos.saveddata.fighter import Fighter

pyfalog = Logger(__name__)


class GuiRemoveProjectedCommand(wx.Command):
    mapping = {
        'fit': FitRemoveProjectedFitCommand,
        'module': FitRemoveProjectedModuleCommand,
        'fighter': FitRemoveProjectedFighterCommand,
        'drone': FitRemoveProjectedDroneCommand
    }

    def __init__(self, fitID, thing):
        wx.Command.__init__(self, True, "Projected Remove")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        fit = self.sFit.getFit(fitID)

        if isinstance(thing, Drone):
            self.data = DroneInfo(itemID=thing.itemID, amount=1, amountActive=1)
            self.type = 'drone'
        elif isinstance(thing, Module):
            self.type = 'module'
            self.data = fit.projectedModules.index(thing)
        elif isinstance(thing, Fighter):
            self.data = fit.projectedFighters.index(thing)
            self.type = 'fighter'
        else:
            # todo: fix!
            self.data = thing.ID
            self.type = 'fit'

    def Do(self):
        result = False
        # since we can project various types, we need to switch of the fit command. We can't do this switch easily in
        # the fit command since each type might have a different kind of undo, easier to split it out

        cls = self.mapping.get(self.type, None)
        if cls:
            cmd = cls(self.fitID, self.data)
            result = self.internal_history.Submit(cmd)

        if result:
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
