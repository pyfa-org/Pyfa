import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo, DroneInfo, FighterInfo
from .calc.fitAddProjectedModule import FitAddProjectedModuleCommand
from .calc.fitAddProjectedFit import FitAddProjectedFitCommand
from .calc.fitAddProjectedFighter import FitAddProjectedFighterCommand
from .calc.fitAddProjectedDrone import FitAddProjectedDroneCommand
from logbook import Logger
import eos.db
pyfalog = Logger(__name__)


class GuiAddProjectedCommand(wx.Command):
    def __init__(self, fitID, id, type='item'):
        wx.Command.__init__(self, True, "Projected Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.id = id
        self.type = type

    def Do(self):
        result = False
        # since we can project various types, we need to switch of the fit command. We can't do this switch easily in
        # the fit command since each type might have a different kind of undo, easier to split it out
        if self.type == 'item':
            item = eos.db.getItem(self.id, eager=("attributes", "group.category"))

            if item.category.name == "Drone":
                result = self.internal_history.Submit(FitAddProjectedDroneCommand(
                    fitID=self.fitID,
                    droneInfo=DroneInfo(itemID=self.id, amount=1, amountActive=1)))
            elif item.category.name == "Fighter":
                result = self.internal_history.Submit(FitAddProjectedFighterCommand(self.fitID, fighterInfo=FighterInfo(itemID=self.id)))
            else:
                result = self.internal_history.Submit(FitAddProjectedModuleCommand(
                    fitID=self.fitID,
                    modInfo=ModuleInfo(itemID=self.id)))
        elif self.type == 'fit':
            result = self.internal_history.Submit(FitAddProjectedFitCommand(self.fitID, self.id, None))

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
