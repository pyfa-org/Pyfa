import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cart.add import CalcAddCartCommand
from gui.fitCommands.calc.cart.remove import CalcRemoveCartCommand
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModulesCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import CartInfo, InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiLocalModuleToCartCommand(wx.Command):

    def __init__(self, fitID, modPosition, cartItemID, copy):
        wx.Command.__init__(self, True, 'Local Module to Cart')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.srcModPosition = modPosition
        self.dstCartItemID = cartItemID
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
        dstCart = next((c for c in fit.cart if c.itemID == self.dstCartItemID), None)
        success = False
        # Attempt to swap if we're moving our module onto a module in the cart hold
        if not self.copy and dstCart is not None and dstCart.item.isModule:
            if srcModItemID == self.dstCartItemID:
                return False
            srcModSlot = srcMod.slot
            newModInfo = ModuleInfo.fromModule(srcMod, unmutate=True)
            newModInfo.itemID = self.dstCartItemID
            srcModChargeItemID = srcMod.chargeID
            srcModChargeAmount = srcMod.numCharges
            commands = []
            commands.append(CalcRemoveCartCommand(
                fitID=self.fitID,
                cartInfo=CartInfo(itemID=self.dstCartItemID, amount=1)))
            commands.append(CalcAddCartCommand(
                fitID=self.fitID,
                # We cannot put mutated items to cart, so use unmutated item ID
                cartInfo=CartInfo(itemID=ModuleInfo.fromModule(srcMod, unmutate=True).itemID, amount=1)))
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
                    # If we had to unload charge, add it to cart
                    if cmdReplace.unloadedCharge and srcModChargeItemID is not None:
                        cmdAddCartCharge = CalcAddCartCommand(
                            fitID=self.fitID,
                            cartInfo=CartInfo(itemID=srcModChargeItemID, amount=srcModChargeAmount))
                        success = self.internalHistory.submit(cmdAddCartCharge)
                    # If we did not unload charge and there still was a charge, see if amount differs and process it
                    elif not cmdReplace.unloadedCharge and srcModChargeItemID is not None:
                        # How many extra charges do we need to take from cart
                        extraChargeAmount = newMod.numCharges - srcModChargeAmount
                        if extraChargeAmount > 0:
                            cmdRemoveCartExtraCharge = CalcRemoveCartCommand(
                                fitID=self.fitID,
                                cartInfo=CartInfo(itemID=srcModChargeItemID, amount=extraChargeAmount))
                            # Do not check if operation was successful or not, we're okay if we have no such
                            # charges in cart
                            self.internalHistory.submit(cmdRemoveCartExtraCharge)
                        elif extraChargeAmount < 0:
                            cmdAddCartExtraCharge = CalcAddCartCommand(
                                fitID=self.fitID,
                                cartInfo=CartInfo(itemID=srcModChargeItemID, amount=abs(extraChargeAmount)))
                            success = self.internalHistory.submit(cmdAddCartExtraCharge)
                    if success:
                        # Store info to properly send events later
                        self.removedModItemID = srcModItemID
                        self.addedModItemID = self.dstCartItemID
                # If drag happened to module which cannot be fit into current slot - consider it as failure
                else:
                    success = False
                # And in case of any failures, cancel everything to try to do move instead
                if not success:
                    self.internalHistory.undoAll()
        # Just dump module and its charges into cart when copying or moving to cart
        if not success:
            commands = []
            commands.append(CalcAddCartCommand(
                fitID=self.fitID,
                cartInfo=CartInfo(itemID=ModuleInfo.fromModule(srcMod, unmutate=True).itemID, amount=1)))
            if srcMod.chargeID is not None:
                commands.append(CalcAddCartCommand(
                    fitID=self.fitID,
                    cartInfo=CartInfo(itemID=srcMod.chargeID, amount=srcMod.numCharges)))
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
