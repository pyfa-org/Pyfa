from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from eos.saveddata.booster import Booster
from eos.saveddata.cargo import Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
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
            mod = Module(item, baseItem=baseItem, mutaplasmid=mutaplasmid)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None

        if self.mutations is not None:
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


class BoosterInfo:

    def __init__(self, itemID, state=None, sideEffects=None):
        self.itemID = itemID
        self.state = state
        self.sideEffects = sideEffects

    @classmethod
    def fromBooster(cls, booster):
        if booster is None:
            return None
        info = cls(
            itemID=booster.itemID,
            state=booster.active,
            sideEffects={se.effectID: se.active for se in booster.sideEffects})
        return info

    def toBooster(self):
        item = Market.getInstance().getItem(self.itemID)
        try:
            booster = Booster(item)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None
        if self.state is not None:
            booster.active = self.state
        if self.sideEffects is not None:
            for sideEffect in booster.sideEffects:
                sideEffect.active = self.sideEffects.get(sideEffect.effectID, sideEffect.active)
        return booster

class CargoInfo:

    def __init__(self, itemID, amount):
        self.itemID = itemID
        self.amount = amount

    def toCargo(self):
        item = Market.getInstance().getItem(self.itemID)
        cargo = Cargo(item)
        cargo.amount = self.amount
        return cargo

    def __repr__(self):
        return makeReprStr(self, ['itemID', 'amount'])


class DroneInfo:

    def __init__(self, itemID, amount, amountActive):
        self.itemID = itemID
        self.amount = amount
        self.amountActive = amountActive

    @classmethod
    def fromDrone(cls, drone):
        if drone is None:
            return None
        info = cls(
            itemID=drone.itemID,
            amount=drone.amount,
            amountActive=drone.amountActive)
        return info

    def toDrone(self):
        item = Market.getInstance().getItem(self.itemID)
        try:
            drone = Drone(item)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None
        drone.amount = self.amount
        drone.amountActive = self.amountActive
        return drone

    def __repr__(self):
        return makeReprStr(self, ['itemID', 'amount', 'amountActive'])


class FighterInfo:

    def __init__(self, itemID, amount=None, state=None, abilities=None):
        self.itemID = itemID
        self.amount = amount
        self.state = state
        self.abilities = abilities

    @classmethod
    def fromFighter(cls, fighter):
        if fighter is None:
            return None
        info = cls(
            itemID=fighter.itemID,
            amount=fighter.amount,
            state=fighter.active,
            abilities={fa.effectID: fa.active for fa in fighter.abilities})
        return info

    def toFighter(self):
        item = Market.getInstance().getItem(self.itemID)
        try:
            fighter = Fighter(item)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None
        if self.amount is not None:
            fighter.amount = self.amount
        if self.state is not None:
            fighter.active = self.state
        if self.abilities is not None:
            for ability in fighter.abilities:
                ability.active = self.abilities.get(ability.effectID, ability.active)
        return fighter

    def __repr__(self):
        return makeReprStr(self, ['itemID', 'amount', 'state', 'abilities'])


def stateLimit(itemIdentity):
    item = Market.getInstance().getItem(itemIdentity)
    if {'moduleBonusAssaultDamageControl', 'moduleBonusIndustrialInvulnerability'}.intersection(item.effects):
        return FittingModuleState.ONLINE
    return FittingModuleState.ACTIVE
