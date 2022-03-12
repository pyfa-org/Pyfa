import math

import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState
from eos.saveddata.booster import Booster
from eos.saveddata.cargo import Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.implant import Implant
from eos.saveddata.module import Module
from service.market import Market
from utils.repr import makeReprStr


pyfalog = Logger(__name__)


class InternalCommandHistory:

    def __init__(self):
        self.__buffer = wx.CommandProcessor()

    def submit(self, command):
        return self.__buffer.Submit(command)

    def submitBatch(self, *commands):
        for command in commands:
            if not self.__buffer.Submit(command):
                # Undo what we already submitted
                for commandToUndo in reversed(self.__buffer.Commands):
                    if commandToUndo in commands:
                        self.__buffer.Undo()
                return False
        return True

    def undoAll(self):
        undoneCommands = []
        # Undo commands one by one, starting from the last
        for commandToUndo in reversed(self.__buffer.Commands):
            if commandToUndo.Undo():
                undoneCommands.append(commandToUndo)
            # If undoing fails, redo already undone commands, starting from the last undone
            else:
                for commandToRedo in reversed(undoneCommands):
                    if not commandToRedo.Do():
                        break
                self.__buffer.ClearCommands()
                return False
        self.__buffer.ClearCommands()
        return True

    def __len__(self):
        return len(self.__buffer.Commands)


class ModuleInfo:

    def __init__(
            self, itemID, baseItemID=None, mutaplasmidID=None, mutations=None, chargeID=None,
            state=None, spoolType=None, spoolAmount=None, rahPattern=None):
        self.itemID = itemID
        self.baseItemID = baseItemID
        self.mutaplasmidID = mutaplasmidID
        self.mutations = mutations
        self.chargeID = chargeID
        self.state = state
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount
        self.rahPattern = rahPattern

    @classmethod
    def fromModule(cls, mod, unmutate=False):
        if mod is None:
            return None
        if unmutate and mod.isMutated:
            info = cls(
                itemID=mod.baseItemID,
                baseItemID=None,
                mutaplasmidID=None,
                mutations={},
                chargeID=mod.chargeID,
                state=mod.state,
                spoolType=mod.spoolType,
                spoolAmount=mod.spoolAmount,
                rahPattern=mod.rahPatternOverride)
        else:
            info = cls(
                itemID=mod.itemID,
                baseItemID=mod.baseItemID,
                mutaplasmidID=mod.mutaplasmidID,
                mutations={m.attrID: m.value for m in mod.mutators.values()},
                chargeID=mod.chargeID,
                state=mod.state,
                spoolType=mod.spoolType,
                spoolAmount=mod.spoolAmount,
                rahPattern=mod.rahPatternOverride)
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

        mod.rahPatternOverride = self.rahPattern

        if self.state is not None:
            if mod.isValidState(self.state):
                mod.state = self.state
            else:
                mod.state = mod.getMaxState(proposedState=self.state)
        elif fallbackState is not None:
            if mod.isValidState(fallbackState):
                mod.state = fallbackState

        if self.chargeID is not None:
            charge = mkt.getItem(self.chargeID, eager=('attributes',))
            if charge is None:
                pyfalog.warning('Cannot set charge {}'.format(self.chargeID))
                return None
            mod.charge = charge

        return mod

    def __eq__(self, other):
        if not isinstance(other, ModuleInfo):
            return False
        return all((
            self.itemID == other.itemID,
            self.baseItemID == other.baseItemID,
            self.mutaplasmidID == other.mutaplasmidID,
            self.mutations == other.mutations,
            self.chargeID == other.chargeID,
            self.state == other.state,
            self.spoolType == other.spoolType,
            self.spoolAmount == other.spoolAmount,
            self.rahPattern == other.rahPattern))

    def __repr__(self):
        return makeReprStr(self, [
            'itemID', 'baseItemID', 'mutaplasmidID', 'mutations',
            'chargeID', 'state', 'spoolType', 'spoolAmount', 'rahPattern'])


class DroneInfo:

    def __init__(self, amount, amountActive, itemID, baseItemID=None, mutaplasmidID=None, mutations=None):
        self.itemID = itemID
        self.baseItemID = baseItemID
        self.mutaplasmidID = mutaplasmidID
        self.mutations = mutations
        self.amount = amount
        self.amountActive = amountActive

    @classmethod
    def fromDrone(cls, drone):
        if drone is None:
            return None
        info = cls(
            itemID=drone.itemID,
            amount=drone.amount,
            amountActive=drone.amountActive,
            baseItemID=drone.baseItemID,
            mutaplasmidID=drone.mutaplasmidID,
            mutations={m.attrID: m.value for m in drone.mutators.values()})
        return info

    def toDrone(self):
        mkt = Market.getInstance()
        item = mkt.getItem(self.itemID, eager=('attributes', 'group.category'))
        if self.baseItemID and self.mutaplasmidID:
            baseItem = mkt.getItem(self.baseItemID, eager=('attributes', 'group.category'))
            mutaplasmid = eos.db.getDynamicItem(self.mutaplasmidID)
        else:
            baseItem = None
            mutaplasmid = None
        try:
            drone = Drone(item, baseItem=baseItem, mutaplasmid=mutaplasmid)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None

        if self.mutations is not None:
            for attrID, mutator in drone.mutators.items():
                if attrID in self.mutations:
                    mutator.value = self.mutations[attrID]

        drone.amount = self.amount
        drone.amountActive = self.amountActive
        return drone

    def __repr__(self):
        return makeReprStr(self, [
            'itemID', 'amount', 'amountActive',
            'baseItemID', 'mutaplasmidID', 'mutations'])


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
        item = Market.getInstance().getItem(self.itemID, eager=('attributes', 'group.category'))
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


class ImplantInfo:

    def __init__(self, itemID, state=None):
        self.itemID = itemID
        self.state = state

    @classmethod
    def fromImplant(cls, implant):
        if implant is None:
            return None
        info = cls(
            itemID=implant.itemID,
            state=implant.active)
        return info

    def toImplant(self):
        item = Market.getInstance().getItem(self.itemID, eager=('attributes', 'group.category'))
        try:
            implant = Implant(item)
        except ValueError:
            pyfalog.warning('Invalid item: {}'.format(self.itemID))
            return None
        if self.state is not None:
            implant.active = self.state
        return implant

    def __repr__(self):
        return makeReprStr(self, ['itemID', 'state'])


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
        item = Market.getInstance().getItem(self.itemID, eager=('attributes', 'group.category'))
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

    def __repr__(self):
        return makeReprStr(self, ['itemID', 'state', 'sideEffects'])


class CargoInfo:

    def __init__(self, itemID, amount):
        self.itemID = itemID
        self.amount = amount

    @classmethod
    def fromCargo(cls, cargo):
        if cargo is None:
            return None
        info = cls(
            itemID=cargo.itemID,
            amount=cargo.amount)
        return info

    def toCargo(self):
        item = Market.getInstance().getItem(self.itemID)
        cargo = Cargo(item)
        cargo.amount = self.amount
        return cargo

    def __repr__(self):
        return makeReprStr(self, ['itemID', 'amount'])


def activeStateLimit(itemIdentity):
    item = Market.getInstance().getItem(itemIdentity)
    if {
        'moduleBonusAssaultDamageControl', 'moduleBonusIndustrialInvulnerability',
        'microJumpDrive', 'microJumpPortalDrive', 'emergencyHullEnergizer',
        'cynosuralGeneration', 'jumpPortalGeneration', 'jumpPortalGenerationBO',
        'cloneJumpAccepting', 'cloakingWarpSafe', 'cloakingPrototype', 'cloaking',
        'massEntanglerEffect5', 'electronicAttributeModifyOnline', 'targetPassively',
        'cargoScan', 'shipScan', 'surveyScan', 'targetSpectrumBreakerBonus',
        'interdictionNullifierBonus', 'warpCoreStabilizerActive',
        'industrialItemCompression'
    }.intersection(item.effects):
        return FittingModuleState.ONLINE
    return FittingModuleState.ACTIVE


def droneStackLimit(fit, itemIdentity):
    item = Market.getInstance().getItem(itemIdentity)
    hardLimit = max(5, fit.extraAttributes["maxActiveDrones"])
    releaseLimit = fit.getReleaseLimitForDrone(item)
    limit = min(hardLimit, releaseLimit if releaseLimit > 0 else math.inf)
    return limit


def restoreCheckedStates(fit, stateInfo, ignoreModPoss=()):
    if stateInfo is None:
        return
    changedMods, changedProjMods, changedProjDrones = stateInfo
    for pos, state in changedMods.items():
        if pos in ignoreModPoss:
            continue
        fit.modules[pos].state = state
    for pos, state in changedProjMods.items():
        fit.projectedModules[pos].state = state
    for pos, amountActive in changedProjDrones.items():
        fit.projectedDrones[pos].amountActive = amountActive


def restoreRemovedDummies(fit, dummyInfo):
    if dummyInfo is None:
        return
    # Need this to properly undo the case when removal of subsystems removes dummy slots
    for position in sorted(dummyInfo):
        slot = dummyInfo[position]
        fit.modules.insert(position, Module.buildEmpty(slot))


def getSimilarModPositions(mods, mainMod):
    sMkt = Market.getInstance()
    mainGroupID = getattr(sMkt.getGroupByItem(mainMod.item), 'ID', None)
    mainMktGroupID = getattr(sMkt.getMarketGroupByItem(mainMod.item), 'ID', None)
    mainEffects = set(getattr(mainMod.item, 'effects', ()))
    positions = []
    for position, mod in enumerate(mods):
        if mod.isEmpty:
            continue
        # Always include selected module itself
        if mod is mainMod:
            positions.append(position)
            continue
        if mod.itemID is None:
            continue
        # Modules which have the same item ID
        if mod.itemID == mainMod.itemID:
            positions.append(position)
            continue
        # And modules from the same group and market group too
        modGroupID = getattr(sMkt.getGroupByItem(mod.item), 'ID', None)
        modMktGroupID = getattr(sMkt.getMarketGroupByItem(mod.item), 'ID', None)
        modEffects = set(getattr(mod.item, 'effects', ()))
        if (
            modGroupID is not None and modGroupID == mainGroupID and
            modMktGroupID is not None and modMktGroupID == mainMktGroupID and
            modEffects == mainEffects
        ):
            positions.append(position)
            continue
    return positions


def getSimilarFighters(fighters, mainFighter):
    sMkt = Market.getInstance()
    mainGroupID = getattr(sMkt.getGroupByItem(mainFighter.item), 'ID', None)
    mainAbilityIDs = set(a.effectID for a in mainFighter.abilities)
    similarFighters = []
    for fighter in fighters:
        # Always include selected fighter itself
        if fighter is mainFighter:
            similarFighters.append(fighter)
            continue
        if fighter.itemID is None:
            continue
        # Fighters which have the same item ID
        if fighter.itemID == mainFighter.itemID:
            similarFighters.append(fighter)
            continue
        # And fighters from the same group and with the same abilities too
        fighterGroupID = getattr(sMkt.getGroupByItem(fighter.item), 'ID', None)
        fighterAbilityIDs = set(a.effectID for a in fighter.abilities)
        if (
            fighterGroupID is not None and fighterGroupID == mainGroupID and
            len(fighterAbilityIDs) > 0 and fighterAbilityIDs == mainAbilityIDs
        ):
            similarFighters.append(fighter)
            continue
    return similarFighters
