import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo, DroneInfo, FighterInfo
from .calcCommands.module.projectedAdd import CalcAddProjectedModuleCommand
from .calcCommands.projectedFit.add import CalcAddProjectedFitCommand
from .calcCommands.fighter.projectedAdd import CalcAddProjectedFighterCommand
from .calcCommands.drone.projectedAdd import CalcAddProjectedDroneCommand
from logbook import Logger
import eos.db
pyfalog = Logger(__name__)


class GuiAddProjectedCommand(wx.Command):
    def __init__(self, fitID, id, type='item'):
        wx.Command.__init__(self, True, "Projected Add")
        self.internalHistory = wx.CommandProcessor()
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
                result = self.internalHistory.Submit(CalcAddProjectedDroneCommand(
                    fitID=self.fitID,
                    droneInfo=DroneInfo(itemID=self.id, amount=1, amountActive=1)))
            elif item.category.name == "Fighter":
                result = self.internalHistory.Submit(CalcAddProjectedFighterCommand(self.fitID, fighterInfo=FighterInfo(itemID=self.id)))
            else:
                result = self.internalHistory.Submit(CalcAddProjectedModuleCommand(
                    fitID=self.fitID,
                    modInfo=ModuleInfo(itemID=self.id)))
        elif self.type == 'fit':
            result = self.internalHistory.Submit(CalcAddProjectedFitCommand(self.fitID, self.id, None))

        if result:
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
