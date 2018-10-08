import wx
from logbook import Logger

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fitRemoveCargo import FitRemoveCargoCommand
from gui.fitCommands.calc.fitRemoveModule import FitRemoveModuleCommand
from gui.fitCommands.calc.fitReplaceModule import FitReplaceModuleCommand
from service.fit import Fit
from .calc.fitAddCargo import FitAddCargoCommand

pyfalog = Logger(__name__)


class GuiModuleToCargoCommand(wx.Command):
    def __init__(self, fitID, moduleIdx, cargoIdx, copy=False):
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.moduleIdx = moduleIdx
        self.cargoIdx = cargoIdx
        self.copy = copy
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        module = fit.modules[self.moduleIdx]
        result = False

        if self.cargoIdx:  # we're swapping with cargo
            if self.copy:  # if copying, simply add item to cargo
                result = self.internal_history.Submit(FitAddCargoCommand(
                    self.mainFrame.getActiveFit(), module.item.ID if not module.item.isAbyssal else module.baseItemID))
            else:  # otherwise, try to swap by replacing module with cargo item. If successful, remove old cargo and add new cargo

                cargo = fit.cargo[self.cargoIdx]
                self.modReplaceCmd = FitReplaceModuleCommand(self.fitID, module.modPosition, cargo.itemID)

                result = self.internal_history.Submit(self.modReplaceCmd)

                if not result:
                    # creating module failed for whatever reason
                    return False

                if self.modReplaceCmd.old_module is not None:
                    # we're swapping with an existing module, so remove cargo and add module
                    self.removeCmd = FitRemoveCargoCommand(self.fitID, cargo.itemID)
                    result = self.internal_history.Submit(self.removeCmd)

                    self.addCargoCmd = FitAddCargoCommand(self.fitID, self.modReplaceCmd.old_module.itemID)
                    result = self.internal_history.Submit(self.addCargoCmd)

        else:  # dragging to blank spot, append
            result = self.internal_history.Submit(FitAddCargoCommand(self.mainFrame.getActiveFit(),
                                                            module.item.ID if not module.item.isAbyssal else module.baseItemID))

            if not self.copy:  # if not copying, remove module
                self.internal_history.Submit(FitRemoveModuleCommand(self.mainFrame.getActiveFit(), [self.moduleIdx]))

        if result:
            sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=module.item.ID))

        return result

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
