import wx
from logbook import Logger

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.calcCommands.module.localRemove import CalcRemoveLocalModuleCommand
from gui.fitCommands.calcCommands.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import ModuleInfo
from service.fit import Fit
from .calcCommands.cargo.add import CalcAddCargoCommand

pyfalog = Logger(__name__)


class GuiModuleToCargoCommand(wx.Command):

    def __init__(self, fitID, moduleIdx, cargoIdx, copy=False):
        wx.Command.__init__(self, True, "Module to Cargo")
        self.fitID = fitID
        self.moduleIdx = moduleIdx
        self.cargoIdx = cargoIdx
        self.copy = copy
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        module = fit.modules[self.moduleIdx]
        result = False

        if self.cargoIdx:  # we're swapping with cargo
            if self.copy:  # if copying, simply add item to cargo
                result = self.internalHistory.Submit(CalcAddCargoCommand(
                    gui.mainFrame.MainFrame.getInstance().getActiveFit(), module.item.ID if not module.item.isAbyssal else module.baseItemID))
            else:  # otherwise, try to swap by replacing module with cargo item. If successful, remove old cargo and add new cargo

                cargo = fit.cargo[self.cargoIdx]
                self.modReplaceCmd = CalcReplaceLocalModuleCommand(
                    fitID=self.fitID,
                    position=module.modPosition,
                    newModInfo=ModuleInfo(itemID=cargo.itemID))

                result = self.internalHistory.Submit(self.modReplaceCmd)

                if not result:
                    # creating module failed for whatever reason
                    return False

                if self.modReplaceCmd.old_module is not None:
                    # we're swapping with an existing module, so remove cargo and add module
                    self.removeCmd = CalcRemoveCargoCommand(self.fitID, cargo.itemID)
                    result = self.internalHistory.Submit(self.removeCmd)

                    self.addCargoCmd = CalcAddCargoCommand(self.fitID, self.modReplaceCmd.old_module.itemID)
                    result = self.internalHistory.Submit(self.addCargoCmd)

        else:  # dragging to blank spot, append
            result = self.internalHistory.Submit(CalcAddCargoCommand(gui.mainFrame.MainFrame.getInstance().getActiveFit(),
                                                                      module.item.ID if not module.item.isAbyssal else module.baseItemID))

            if not self.copy:  # if not copying, remove module
                self.internalHistory.Submit(CalcRemoveLocalModuleCommand(gui.mainFrame.MainFrame.getInstance().getActiveFit(), [self.moduleIdx]))

        if result:
            sFit.recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action="moddel", typeID=module.item.ID))

        return result

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
