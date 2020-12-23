import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiCargoToLocalModuleCommand(wx.Command):
    """
    Moves cargo to the fitting window. If target is not empty, take whatever we take off and put
    into the cargo hold. If we copy, we do the same but do not remove the item from the cargo hold.
    """

    def __init__(self, fitID, cargoItemID, modPosition, copy):
        wx.Command.__init__(self, True, 'Cargo to Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.srcCargoItemID = cargoItemID
        self.dstModPosition = modPosition
        self.copy = copy
        self.removedModItemID = None
        self.addedModItemID = None
        self.savedRemovedDummies = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        srcCargo = next((c for c in fit.cargo if c.itemID == self.srcCargoItemID), None)
        if srcCargo is None:
            return False
        dstMod = fit.modules[self.dstModPosition]
        # Moving/copying charge from cargo to fit
        if srcCargo.item.isCharge and not dstMod.isEmpty:
            newCargoChargeItemID = dstMod.chargeID
            newCargoChargeAmount = dstMod.numCharges
            newModChargeItemID = self.srcCargoItemID
            newModChargeAmount = dstMod.getNumCharges(srcCargo.item)
            if newCargoChargeItemID == newModChargeItemID:
                return False
            commands = []
            if not self.copy:
                commands.append(CalcRemoveCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=newModChargeItemID, amount=newModChargeAmount)))
            if newCargoChargeItemID is not None:
                commands.append(CalcAddCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=newCargoChargeItemID, amount=newCargoChargeAmount)))
            commands.append(CalcChangeModuleChargesCommand(
                fitID=self.fitID,
                projected=False,
                chargeMap={self.dstModPosition: self.srcCargoItemID}))
            success = self.internalHistory.submitBatch(*commands)
        # Moving/copying/replacing module
        elif srcCargo.item.isModule:
            dstModItemID = dstMod.itemID
            dstModSlot = dstMod.slot
            if self.srcCargoItemID == dstModItemID:
                return False
            # To keep all old item properties, copy them over from old module, except for mutations
            newModInfo = ModuleInfo.fromModule(dstMod, unmutate=True)
            newModInfo.itemID = self.srcCargoItemID
            if dstMod.isEmpty:
                newCargoModItemID = None
                dstModChargeItemID = None
                dstModChargeAmount = None
            else:
                # We cannot put mutated items to cargo, so use unmutated item ID
                newCargoModItemID = ModuleInfo.fromModule(dstMod, unmutate=True).itemID
                dstModChargeItemID = dstMod.chargeID
                dstModChargeAmount = dstMod.numCharges
            commands = []
            # Keep cargo only in case we were copying
            if not self.copy:
                commands.append(CalcRemoveCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=self.srcCargoItemID, amount=1)))
            # Add item to cargo only if we copied/moved to non-empty slot
            if newCargoModItemID is not None:
                commands.append(CalcAddCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=newCargoModItemID, amount=1)))
            cmdReplace = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=self.dstModPosition,
                newModInfo=newModInfo,
                unloadInvalidCharges=True)
            commands.append(cmdReplace)
            # Submit batch now because we need to have updated info on fit to keep going
            success = self.internalHistory.submitBatch(*commands)
            newMod = fit.modules[self.dstModPosition]
            # Bail if drag happened to slot to which module cannot be dragged, will undo later
            if newMod.slot != dstModSlot:
                success = False
            if success:
                # If we had to unload charge, add it to cargo
                if cmdReplace.unloadedCharge and dstModChargeItemID is not None:
                    cmdAddCargoCharge = CalcAddCargoCommand(
                        fitID=self.fitID,
                        cargoInfo=CargoInfo(itemID=dstModChargeItemID, amount=dstModChargeAmount))
                    success = self.internalHistory.submit(cmdAddCargoCharge)
                # If we did not unload charge and there still was a charge, see if amount differs and process it
                elif not cmdReplace.unloadedCharge and dstModChargeItemID is not None:
                    # How many extra charges do we need to take from cargo
                    extraChargeAmount = newMod.numCharges - dstModChargeAmount
                    if extraChargeAmount > 0:
                        cmdRemoveCargoExtraCharge = CalcRemoveCargoCommand(
                            fitID=self.fitID,
                            cargoInfo=CargoInfo(itemID=dstModChargeItemID, amount=extraChargeAmount))
                        # Do not check if operation was successful or not, we're okay if we have no such
                        # charges in cargo
                        self.internalHistory.submit(cmdRemoveCargoExtraCharge)
                    elif extraChargeAmount < 0:
                        cmdAddCargoExtraCharge = CalcAddCargoCommand(
                            fitID=self.fitID,
                            cargoInfo=CargoInfo(itemID=dstModChargeItemID, amount=abs(extraChargeAmount)))
                        success = self.internalHistory.submit(cmdAddCargoExtraCharge)
            if success:
                # Store info to properly send events later
                self.removedModItemID = dstModItemID
                self.addedModItemID = self.srcCargoItemID
            else:
                self.internalHistory.undoAll()
        else:
            return False
        eos.db.flush()
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
