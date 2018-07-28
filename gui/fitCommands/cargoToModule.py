import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.fitSetCharge import FitSetChargeCommand
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
        # todo: instead of modules, needs to be positions. Dead objects are a thing
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
        cargo = fit.cargo[self.cargoIdx]
        result = None

        # We're trying to move a charge from cargo to a slot. Use SetCharge command (don't respect move vs copy)
        if sFit.isAmmo(cargo.item.ID):
            result = self.internal_history.Submit(FitSetChargeCommand(self.fitID, [module], cargo.item.ID))
        # else:
        #
        #     pyfalog.debug("Moving cargo item to module for fit ID: {0}", self.fitID)
        #
        #     # Gather modules and convert Cargo item to Module, silently return if not a module
        #     try:
        #         cargoP = es_Module(cargo.item)
        #         cargoP.owner = fit
        #         if cargoP.isValidState(State.ACTIVE):
        #             cargoP.state = State.ACTIVE
        #     except:
        #         pyfalog.warning("Invalid item: {0}", cargo.item)
        #         return
        #
        #     if cargoP.slot != module.slot:  # can't swap modules to different racks
        #         return
        #
        #     # remove module that we are trying to move cargo to
        #     fit.modules.remove(module)
        #
        #     if not cargoP.fits(fit):  # if cargo doesn't fit, rollback and return
        #         fit.modules.insert(moduleIdx, module)
        #         return
        #
        #     fit.modules.insert(moduleIdx, cargoP)
        #
        #     if not copyMod:  # remove existing cargo if not cloning
        #         if cargo.amount == 1:
        #             fit.cargo.remove(cargo)
        #         else:
        #             cargo.amount -= 1
        #
        #     if not module.isEmpty:  # if module is placeholder, we don't want to convert/add it
        #         moduleItem = module.item if not module.item.isAbyssal else module.baseItem
        #         for x in fit.cargo.find(moduleItem):
        #             x.amount += 1
        #             break
        #         else:
        #             moduleP = es_Cargo(moduleItem)
        #             moduleP.amount = 1
        #             fit.cargo.insert(cargoIdx, moduleP)
        #
        #     eos.db.commit()
        #     self.recalc(fit)
        # #
        # #
        # #
        # # if self.clone:
        # #     result = self.internal_history.Submit(FitCloneModduleCommand(self.fitID, self.srcPosition, self.dstPosition))
        # # else:
        # #     result = self.internal_history.Submit(FitSwapModuleCommand(self.fitID, self.srcPosition, self.dstPosition))

        if result:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return result

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
