import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitRemoveProjectedModule import FitRemoveProjectedModuleCommand
from .calc.fitRemoveProjectedEnv import FitRemoveProjectedEnvCommand
from .calc.fitRemoveProjectedFit import FitRemoveProjectedFitCommand
from .calc.fitRemoveProjectedFighter import FitRemoveProjectedFighterCommand
from logbook import Logger
from .calc.fitRemoveProjectedDrone import FitRemoveProjectedDroneCommand

from eos.saveddata.drone import Drone
from eos.saveddata.module import Module
from eos.saveddata.fighter import Fighter

pyfalog = Logger(__name__)


class GuiRemoveProjectedCommand(wx.Command):
    mapping = {
        'fit': FitRemoveProjectedFitCommand,
        'module': FitRemoveProjectedModuleCommand,
        'fighter': FitRemoveProjectedFighterCommand,
        'env': FitRemoveProjectedEnvCommand,
        'drone': FitRemoveProjectedDroneCommand
    }

    def __init__(self, fitID, thing):
        wx.Command.__init__(self, True, "Projected Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        fit = self.sFit.getFit(fitID)

        if isinstance(thing, Drone):
            self.data = fit.projectedDrones.index(thing)
            self.type = 'drone'
        elif isinstance(thing, Module):
            # todo: projected stuff should be wrapped in a projected class wrapper for easier maintainence
            if thing.item.group.name in Module.SYSTEM_GROUPS:
                self.type = 'env'
                self.data = thing.itemID
            else:
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

        # if item.category.name == "Drone":
        #     pyfalog.warn("DRONE REMOVE PROJECTION NOT IMPLEMENTED")
        # elif item.category.name == "Fighter":
        #     pyfalog.warn("FIGHTER REMOVE PROJECTION NOT IMPLEMENTED")
        # elif item.group.name in Module.SYSTEM_GROUPS:
        #     result = self.internal_history.Submit(FitRemoveProjectedEnvCommand(self.fitID, self.id))
        # else:
        #     # attempt a regular module projection
        #
        # elif self.type == 'fit':
        #     pyfalog.warn("FIT REMOVE PROJECTION NOT IMPLEMENTED")

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
