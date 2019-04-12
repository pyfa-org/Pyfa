from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from eos.saveddata.module import Module
from service.market import Market
from utils.repr import makeReprStr


pyfalog = Logger(__name__)


class ModuleInfo:

    def __init__(self, itemID, baseItemID=None, mutaplasmidID=None, mutations=None, chargeID=None, state=None, spoolType=None, spoolAmount=None):
        self.itemID = itemID
        self.baseItemID = baseItemID
        self.mutaplasmidID = mutaplasmidID
        self.mutations = mutations
        self.chargeID = chargeID
        self.state = state
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount

    @classmethod
    def fromModule(cls, mod):
        if mod is None:
            return None
        info = cls(
            itemID=mod.itemID,
            baseItemID=mod.baseItemID,
            mutaplasmidID=mod.mutaplasmidID,
            mutations={m.attrID: m.value for m in mod.mutators.values()},
            chargeID=mod.chargeID,
            state=mod.state,
            spoolType=mod.spoolType,
            spoolAmount=mod.spoolAmount)
        return info

    def toModule(self, fallbackState=None):
        mkt = Market.getInstance()

        item = mkt.getItem(self.itemID, eager=('attributes', 'group.category'))
        if self.baseItemID and self.mutaplasmidID:
            baseItem = mkt.getItem(self.baseItemID, eager=('attributes', 'group.category'))
            mutaplasmid = eos.db.getDynamicItem(self.mutaplasmidID)
        else:
            baseItem = None
            mutaplasmid = None
        try:
            mod = Module(item, baseItem, mutaplasmid)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None

        for attrID, mutator in mod.mutators.items():
            if attrID in self.mutations:
                mutator.value = self.mutations[attrID]

        if self.spoolType is not None and self.spoolAmount is not None:
            mod.spoolType = self.spoolType
            mod.spoolAmount = self.spoolAmount

        if self.state is not None:
            if not mod.isValidState(self.state):
                pyfalog.warning('Cannot set state {}'.format(self.state))
                return None
            mod.state = self.state
        elif fallbackState is not None:
            if mod.isValidState(fallbackState):
                mod.state = fallbackState

        if self.chargeID is not None:
            charge = mkt.getItem(self.chargeID)
            if charge is None:
                pyfalog.warning('Cannot set charge {}'.format(self.chargeID))
                return None
            mod.charge = charge

        return mod

    def __repr__(self):
        return makeReprStr(self, [
            'itemID', 'baseItemID', 'mutaplasmidID', 'mutations',
            'chargeID', 'state', 'spoolType', 'spoolAmount'])


def stateLimit(itemIdentity):
    item = Market.getInstance().getItem(itemIdentity)
    if {'moduleBonusAssaultDamageControl', 'moduleBonusIndustrialInvulnerability'}.intersection(item.effects):
        return FittingModuleState.ONLINE
    return FittingModuleState.ACTIVE
