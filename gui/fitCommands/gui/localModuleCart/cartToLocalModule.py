import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cart.add import CalcAddCartCommand
from gui.fitCommands.calc.cart.remove import CalcRemoveCartCommand
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import CartInfo, InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiCartToLocalModuleCommand(wx.Command):
    """
    Moves cart to the fitting window. If target is not empty, take whatever we take off and put
    into the cart hold. If we copy, we do the same but do not remove the item from the cart hold.
    """

    def __init__(self, fitID, cartItemID, modPosition, copy):
        wx.Command.__init__(self, True, 'Cart to Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.srcCartItemID = cartItemID
        self.dstModPosition = modPosition
        self.copy = copy
        self.removedModItemID = None
        self.addedModItemID = None
        self.savedRemovedDummies = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        srcCart = next((c for c in fit.cart if c.itemID == self.srcCartItemID), None)
        if srcCart is None:
            return False
        dstMod = fit.modules[self.dstModPosition]
        # Moving/copying charge from cart to fit
        if srcCart.item.isCharge and not dstMod.isEmpty:
            newCartChargeItemID = dstMod.chargeID
            newCartChargeAmount = dstMod.numCharges
            newModChargeItemID = self.srcCartItemID
            newModChargeAmount = dstMod.getNumCharges(srcCart.item)
            if newCartChargeItemID == newModChargeItemID:
                return False
            commands = []
            if not self.copy:
                commands.append(CalcRemoveCartCommand(
                    fitID=self.fitID,
                    cartInfo=CartInfo(itemID=newModChargeItemID, amount=newModChargeAmount)))
            if newCartChargeItemID is not None:
                commands.append(CalcAddCartCommand(
                    fitID=self.fitID,
                    cartInfo=CartInfo(itemID=newCartChargeItemID, amount=newCartChargeAmount)))
            commands.append(CalcChangeModuleChargesCommand(
                fitID=self.fitID,
                projected=False,
                chargeMap={self.dstModPosition: self.srcCartItemID}))
            success = self.internalHistory.submitBatch(*commands)
        # Moving/copying/replacing module
        elif srcCart.item.isModule:
            dstModItemID = dstMod.itemID
            dstModSlot = dstMod.slot
            if self.srcCartItemID == dstModItemID:
                return False
            # To keep all old item properties, copy them over from old module, except for mutations
            newModInfo = ModuleInfo.fromModule(dstMod, unmutate=True)
            newModInfo.itemID = self.srcCartItemID
            if dstMod.isEmpty:
                newCartModItemID = None
                dstModChargeItemID = None
                dstModChargeAmount = None
            else:
                # We cannot put mutated items to cart, so use unmutated item ID
                newCartModItemID = ModuleInfo.fromModule(dstMod, unmutate=True).itemID
                dstModChargeItemID = dstMod.chargeID
                dstModChargeAmount = dstMod.numCharges
            commands = []
            # Keep cart only in case we were copying
            if not self.copy:
                commands.append(CalcRemoveCartCommand(
                    fitID=self.fitID,
                    cartInfo=CartInfo(itemID=self.srcCartItemID, amount=1)))
            # Add item to cart only if we copied/moved to non-empty slot
            if newCartModItemID is not None:
                commands.append(CalcAddCartCommand(
                    fitID=self.fitID,
                    cartInfo=CartInfo(itemID=newCartModItemID, amount=1)))
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
                # If we had to unload charge, add it to cart
                if cmdReplace.unloadedCharge and dstModChargeItemID is not None:
                    cmdAddCartCharge = CalcAddCartCommand(
                        fitID=self.fitID,
                        cartInfo=CartInfo(itemID=dstModChargeItemID, amount=dstModChargeAmount))
                    success = self.internalHistory.submit(cmdAddCartCharge)
                # If we did not unload charge and there still was a charge, see if amount differs and process it
                elif not cmdReplace.unloadedCharge and dstModChargeItemID is not None:
                    # How many extra charges do we need to take from cart
                    extraChargeAmount = newMod.numCharges - dstModChargeAmount
                    if extraChargeAmount > 0:
                        cmdRemoveCartExtraCharge = CalcRemoveCartCommand(
                            fitID=self.fitID,
                            cartInfo=CartInfo(itemID=dstModChargeItemID, amount=extraChargeAmount))
                        # Do not check if operation was successful or not, we're okay if we have no such
                        # charges in cart
                        self.internalHistory.submit(cmdRemoveCartExtraCharge)
                    elif extraChargeAmount < 0:
                        cmdAddCartExtraCharge = CalcAddCartCommand(
                            fitID=self.fitID,
                            cartInfo=CartInfo(itemID=dstModChargeItemID, amount=abs(extraChargeAmount)))
                        success = self.internalHistory.submit(cmdAddCartExtraCharge)
            if success:
                # Store info to properly send events later
                self.removedModItemID = dstModItemID
                self.addedModItemID = self.srcCartItemID
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
