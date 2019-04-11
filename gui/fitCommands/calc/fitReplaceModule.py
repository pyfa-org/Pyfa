import wx
from logbook import Logger

import eos.db
from eos.saveddata.module import Module
from gui.fitCommands.helpers import ModuleInfoCache, stateLimit
from service.fit import Fit
from service.market import Market

pyfalog = Logger(__name__)


class FitReplaceModuleCommand(wx.Command):
    """"
    Fitting command that changes an existing module into another.

    from sFit.changeModule
    """
    def __init__(self, fitID, position, newItemID, newBaseItemID, newMutaplasmidID, newMutations, newState, newChargeID):
        wx.Command.__init__(self, True, "Change Module")
        self.fitID = fitID
        self.position = position
        self.newItemID = newItemID
        self.newBaseItemID = newBaseItemID
        self.newMutaplasmidID = newMutaplasmidID
        self.newMutations = newMutations
        self.newState = newState
        self.newChargeID = newChargeID
        self.oldModuleInfo = None

    def Do(self):
        fit = Fit.getInstance().getFit(self.fitID)
        mod = fit.modules[self.position]
        if not mod.isEmpty:
            self.oldModuleInfo = ModuleInfoCache(
                mod.modPosition,
                mod.item.ID,
                mod.state,
                mod.chargeID,
                mod.baseItemID,
                mod.mutaplasmidID,
                {m.attrID: m.value for m in mod.mutators.values()})

        newState = self.newState if self.newState is not None else getattr(self.oldModuleInfo, 'state', None)
        newChargeID = self.newChargeID if self.newChargeID is not None else getattr(self.oldModuleInfo, 'chargeID', None)
        return self.changeModule(self.newItemID, self.newBaseItemID, self.newMutaplasmidID, self.newMutations, newState, newChargeID)

    def Undo(self):
        if self.oldModuleInfo is None:
            fit = Fit.getInstance().getFit(self.fitID)
            fit.modules.toDummy(self.position)
            return True
        return self.changeModule(
            self.oldModuleInfo.itemID,
            self.oldModuleInfo.baseID,
            self.oldModuleInfo.mutaplasmidID,
            self.oldModuleInfo.mutations,
            self.oldModuleInfo.state,
            self.oldModuleInfo.chargeID)

    def changeModule(self, itemID, baseItemID, mutaplasmidID, mutations, state, chargeID):
        fit = Fit.getInstance().getFit(self.fitID)
        oldMod = fit.modules[self.position]

        pyfalog.debug("Changing module on position ({0}) for fit ID: {1}", self.position, self.fitID)

        mkt = Market.getInstance()
        item = mkt.getItem(itemID, eager=("attributes", "group.category"))
        if baseItemID and mutaplasmidID:
            baseItem = mkt.getItem(baseItemID, eager=("attributes", "group.category"))
            mutaplasmid = eos.db.getDynamicItem(mutaplasmidID)
        else:
            baseItem = None
            mutaplasmid = None

        try:
            newMod = Module(item, baseItem, mutaplasmid)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return False

        if newMod.slot != oldMod.slot:
            return False

        for attrID, mutator in newMod.mutators.items():
            if attrID in mutations:
                mutator.value = mutations[attrID]

        # Dummy it out in case the next bit fails
        fit.modules.toDummy(self.position)

        if not newMod.fits(fit):
            self.Undo()
            return False

        newMod.owner = fit
        fit.modules.toModule(self.position, newMod)

        if state is not None:
            if not newMod.isValidState(state):
                return False
            newMod.state = state
        else:
            desiredState = stateLimit(newMod.item) if state is None else state
            if newMod.isValidState(desiredState):
                newMod.state = desiredState

        if chargeID is not None:
            charge = mkt.getItem(chargeID)
            if charge is not None:
                newMod.charge = charge

        eos.db.commit()
        return True
