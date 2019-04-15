import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import ModuleInfo
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from logbook import Logger
pyfalog = Logger(__name__)


class GuiCargoToModuleCommand(wx.Command):
    """
    Moves cargo to fitting window. Can either do a copy, move, or swap with current module
    If we try to copy/move into a spot with a non-empty module, we swap instead.
    To avoid redundancy in converting Cargo item, this function does the
    sanity checks as opposed to the GUI View. This is different than how the
    normal .swapModules() does things, which is mostly a blind swap.
    """

    def __init__(self, fitID, moduleIdx, cargoIdx, copy=False):
        wx.Command.__init__(self, True, "Cargo to Module")
        self.fitID = fitID
        self.moduleIdx = moduleIdx
        self.cargoIdx = cargoIdx
        self.copy = copy
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        module = fit.modules[self.moduleIdx]
        cargo = fit.cargo[self.cargoIdx]
        result = False

        # We're trying to move a charge from cargo to a slot. Use SetCharge command (don't respect move vs copy)
        if sFit.isAmmo(cargo.itemID):
            result = self.internalHistory.Submit(CalcChangeModuleChargesCommand(self.fitID, False, {module.modPosition: cargo.itemID}))
        else:

            pyfalog.debug("Moving cargo item to module for fit ID: {0}", self.fitID)

            self.addCmd = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=module.modPosition,
                newModInfo=ModuleInfo(itemID=cargo.itemID))

            result = self.internalHistory.Submit(self.addCmd)

            if not result:
                # creating module failed for whatever reason
                return False

            if self.addCmd.old_module is not None:
                # we're swapping with an existing module, so remove cargo and add module
                self.removeCmd = CalcRemoveCargoCommand(self.fitID, cargo.itemID)
                result = self.internalHistory.Submit(self.removeCmd)

                self.addCargoCmd = CalcAddCargoCommand(self.fitID, self.addCmd.old_module.itemID)
                result = self.internalHistory.Submit(self.addCargoCmd)
            elif not self.copy:
                # move, not copying, so remove cargo
                self.removeCmd = CalcRemoveCargoCommand(self.fitID, cargo.itemID)
                result = self.internalHistory.Submit(self.removeCmd)

        if result:
            sFit.recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return result

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
