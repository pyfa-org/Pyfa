import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.calc.module.localRemove import CalcRemoveLocalModuleCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory, ModuleInfo
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

    def Do(self):
        fit = Fit.getInstance().getFit(self.fitID)
        srcMod = fit.modules[self.srcModPosition]
        if srcMod.isEmpty:
            return False
        srcModItemID = srcMod.itemID
        if self.dstCargoItemID == srcModItemID:
            return False
        dstCargo = next((c for c in fit.cargo if c.itemID == self.dstCargoItemID), None)
        newCargoModItemID = srcMod.baseItemID if srcMod.isMutated else srcMod.itemID
        newCargoChargeItemID = srcMod.chargeID
        newCargoChargeAmount = srcMod.numCharges
        # Save module info to do swap is cargo item is module and we're not copying
        if dstCargo is not None and dstCargo.item.isModule and not self.copy:
            newModInfo = ModuleInfo.fromModule(srcMod)
            newModInfo.itemID = self.dstCargoItemID
        else:
            newModInfo = None
        if newModInfo is not None:
            cmdRemoveCargo = CalcRemoveCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=self.dstCargoItemID, amount=1),
                commit=False)
            success = self.internalHistory.submit(cmdRemoveCargo)
            if not success:
                self.internalHistory.undoAll()
                self.__finalizeDo()
                return success
        cmdAddCargoMod = CalcAddCargoCommand(
            fitID=self.fitID,
            cargoInfo=CargoInfo(itemID=newCargoModItemID, amount=1),
            commit=False)
        success = self.internalHistory.submit(cmdAddCargoMod)
        if not success:
            self.internalHistory.undoAll()
            self.__finalizeDo()
            return success
        cmdReplaceMod = None
        removeCargo = False
        if newModInfo is not None:
            removeCargo = True
            cmdReplaceMod = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=self.srcModPosition,
                newModInfo=newModInfo,
                unloadInvalidCharges=True,
                commit=False)
            success = self.internalHistory.submit(cmdReplaceMod)
            # If replace fails, try just removing instead - we need this to be able to drag high-slot modules
            # over low-slot items in cargo, so that module will still be placed in the cargo
            if not success:
                success = True
                cmdReplaceMod = None
                removeCargo = False
        if removeCargo:
            if not self.copy:
                cmdRemoveMod = CalcRemoveLocalModuleCommand(
                    fitID=self.fitID,
                    positions=[self.srcModPosition],
                    commit=False)
                success = self.internalHistory.submit(cmdRemoveMod)
                if not success:
                    self.internalHistory.undoAll()
                    self.__finalizeDo()
                    return success
        # Add charge to cargo only if we had to unload it or we're copying
        if newCargoChargeItemID is not None and ((cmdReplaceMod is not None and cmdReplaceMod.unloadedCharge) or self.copy):
            cmdAddCargoCharge = CalcAddCargoCommand(
                fitID=self.fitID,
                cargoInfo=CargoInfo(itemID=newCargoChargeItemID, amount=newCargoChargeAmount),
                commit=False)
            success = self.internalHistory.submit(cmdAddCargoCharge)
            if not success:
                self.internalHistory.undoAll()
                self.__finalizeDo()
                return success
        if success:
            self.addedModItemID = newModInfo.itemID if newModInfo is not None else None
            self.removedModItemID = srcModItemID
        self.__finalizeDo()
        return success

    def __finalizeDo(self):
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        events = []
        if self.removedModItemID is not None:
            events.append(GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.removedModItemID))
        if self.addedModItemID is not None:
            events.append(GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.addedModItemID))
        if not events:
            events.append(GE.FitChanged(fitID=self.fitID))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        events = []
        if self.addedModItemID is not None:
            events.append(GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.addedModItemID))
        if self.removedModItemID is not None:
            events.append(GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.removedModItemID))
        if not events:
            events.append(GE.FitChanged(fitID=self.fitID))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success
