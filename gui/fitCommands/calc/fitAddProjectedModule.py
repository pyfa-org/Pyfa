import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from eos.saveddata.module import Module
from gui.fitCommands.helpers import ModuleInfoCache
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitAddProjectedModuleCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, newItemID, newBaseItemID, newMutaplasmidID, newMutations, newState, newChargeID, newPosition):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.newItemID = newItemID
        self.newBaseItemID = newBaseItemID
        self.newMutaplasmidID = newMutaplasmidID
        self.newMutations = newMutations
        self.newState = newState
        self.newChargeID = newChargeID
        self.newPosition = newPosition
        self.oldModuleInfo = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.newItemID)
        fit = Fit.getInstance().getFit(self.fitID)
        mod = self.makeModule(self.newItemID, self.newBaseItemID, self.newMutaplasmidID, self.newMutations, self.newState, self.newChargeID)
        if mod is None:
            return False

        if not mod.canHaveState(mod.state, fit):
            mod.state = FittingModuleState.OFFLINE

        oldItemID, oldBaseItemID, oldMutaplasmidID, oldMutations, oldState, oldChargeID, oldPosition = fit.projectedModules.makeRoom(mod)
        if oldItemID is not None:
            self.oldModuleInfo = ModuleInfoCache(oldPosition, oldItemID, oldState, oldChargeID, oldBaseItemID, oldMutaplasmidID, oldMutations)

        if self.newPosition is not None:
            fit.projectedModules.insert(self.newPosition, mod)
        else:
            fit.projectedModules.append(mod)
            self.newPosition = fit.projectedModules.index(mod)

        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedModule import FitRemoveProjectedModuleCommand  # avoids circular import
        cmd = FitRemoveProjectedModuleCommand(self.fitID, self.newPosition)
        cmd.Do()
        return True

    def makeModule(self, itemID, baseItemID, mutaplasmidID, mutations, state, chargeID):
        mkt = Market.getInstance()

        item = mkt.getItem(itemID, eager=("attributes", "group.category"))
        if baseItemID and mutaplasmidID:
            baseItem = mkt.getItem(baseItemID, eager=("attributes", "group.category"))
            mutaplasmid = eos.db.getDynamicItem(mutaplasmidID)
        else:
            baseItem = None
            mutaplasmid = None
        try:
            mod = Module(item, baseItem, mutaplasmid)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return None

        for attrID, mutator in mod.mutators.items():
            if attrID in mutations:
                mutator.value = mutations[attrID]

        if state is not None:
            if not mod.isValidState(state):
                return None
            mod.state = state
        else:
            desiredState = FittingModuleState.ACTIVE
            if mod.isValidState(desiredState):
                mod.state = desiredState

        if chargeID is not None:
            charge = mkt.getItem(chargeID)
            if charge is not None:
                mod.charge = charge

        return mod
