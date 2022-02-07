import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModulesCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiLocalModuleToCargoCommand(wx.Command):

    def __init__(self, fitID, modPosition, cargoItemID, copy):
        wx.Command.__init__(self, True, 'Local Module to Cargo')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.srcModPosition = modPosition
        self.dstCargoItemID = cargoItemID
        self.copy = copy
        self.removedModItemID = None
        self.addedModItemID = None
        self.savedRemovedDummies = None

    def Do(self):
        fit = Fit.getInstance().getFit(self.fitID)
        srcMod = fit.modules[self.srcModPosition]
        if srcMod.isEmpty:
            return False
        srcModItemID = srcMod.itemID
        dstCargo = next((c for c in fit.cargo if c.itemID == self.dstCargoItemID), None)
        success = False
        # Attempt to swap if we're moving our module onto a module in the cargo hold
        if not self.copy and dstCargo is not None and dstCargo.item.isModule:
            if srcModItemID == self.dstCargoItemID:
                return False
            srcModSlot = srcMod.slot
            newModInfo = ModuleInfo.fromModule(srcMod, unmutate=True)
            newModInfo.itemID = self.dstCargoItemID
            srcModChargeItemID = srcMod.chargeID
            srcModChargeAmount = srcMod.numCharges
            commands = []
            commands.append(CalcRemoveCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=self.dstCargoItemID, amount=1)))
            commands.append(CalcAddCargoCommand(
                fitID=self.fitID,
                # We cannot put mutated items to cargo, so use unmutated item ID
                cargoInfo=CargoInfo(itemID=ModuleInfo.fromModule(srcMod, unmutate=True).itemID, amount=1)))
            cmdReplace = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=self.srcModPosition,
                newModInfo=newModInfo,
                unloadInvalidCharges=True)
            commands.append(cmdReplace)
            # Submit batch now because we need to have updated info on fit to keep going
            success = self.internalHistory.submitBatch(*commands)
            if success:
                newMod = fit.modules[self.srcModPosition]
                # Process charge changes if module is moved to proper slot
                if newMod.slot == srcModSlot:
                    # If we had to unload charge, add it to cargo
                    if cmdReplace.unloadedCharge and srcModChargeItemID is not None:
                        cmdAddCargoCharge = CalcAddCargoCommand(
                            fitID=self.fitID,
                            cargoInfo=CargoInfo(itemID=srcModChargeItemID, amount=srcModChargeAmount))
                        success = self.internalHistory.submit(cmdAddCargoCharge)
                    # If we did not unload charge and there still was a charge, see if amount differs and process it
                    elif not cmdReplace.unloadedCharge and srcModChargeItemID is not None:
                        # How many extra charges do we need to take from cargo
                        extraChargeAmount = newMod.numCharges - srcModChargeAmount
                        if extraChargeAmount > 0:
                            cmdRemoveCargoExtraCharge = CalcRemoveCargoCommand(
                                fitID=self.fitID,
                                cargoInfo=CargoInfo(itemID=srcModChargeItemID, amount=extraChargeAmount))
                            # Do not check if operation was successful or not, we're okay if we have no such
                            # charges in cargo
                            self.internalHistory.submit(cmdRemoveCargoExtraCharge)
                        elif extraChargeAmount < 0:
                            cmdAddCargoExtraCharge = CalcAddCargoCommand(
                                fitID=self.fitID,
                                cargoInfo=CargoInfo(itemID=srcModChargeItemID, amount=abs(extraChargeAmount)))
                            success = self.internalHistory.submit(cmdAddCargoExtraCharge)
                    if success:
                        # Store info to properly send events later
                        self.removedModItemID = srcModItemID
                        self.addedModItemID = self.dstCargoItemID
                # If drag happened to module which cannot be fit into current slot - consider it as failure
                else:
                    success = False
                # And in case of any failures, cancel everything to try to do move instead
                if not success:
                    self.internalHistory.undoAll()
        # Just dump module and its charges into cargo when copying or moving to cargo
        if not success:
            commands = []
            commands.append(CalcAddCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=ModuleInfo.fromModule(srcMod, unmutate=True).itemID, amount=1)))
            if srcMod.chargeID is not None:
                commands.append(CalcAddCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=srcMod.chargeID, amount=srcMod.numCharges)))
            if not self.copy:
                commands.append(CalcRemoveLocalModulesCommand(
                    fitID=self.fitID,
                    positions=[self.srcModPosition]))
            success = self.internalHistory.submitBatch(*commands)
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        events = []
        if self.removedModItemID is not None:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.removedModItemID))
        if self.addedModItemID is not None:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.addedModItemID))
        if not events:
            events.append(GE.FitChanged(fitIDs=(self.fitID,)))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        events = []
        if self.addedModItemID is not None:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.addedModItemID))
        if self.removedModItemID is not None:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.removedModItemID))
        if not events:
            events.append(GE.FitChanged(fitIDs=(self.fitID,)))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success
