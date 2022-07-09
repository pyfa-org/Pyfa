# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import math

from logbook import Logger
from sqlalchemy.orm import reconstructor, validates

import eos.db
from eos.const import FittingHardpoint, FittingModuleState, FittingSlot
from eos.effectHandlerHelpers import HandledCharge, HandledItem
from eos.modifiedAttributeDict import ChargeAttrShortcut, ItemAttrShortcut, ModifiedAttributeDict
from eos.saveddata.citadel import Citadel
from eos.saveddata.mutatedMixin import MutatedMixin, MutaError
from eos.saveddata.mutator import MutatorModule
from eos.utils.cycles import CycleInfo, CycleSequence
from eos.utils.default import DEFAULT
from eos.utils.float import floatUnerr
from eos.utils.spoolSupport import calculateSpoolup, resolveSpoolOptions
from eos.utils.stats import DmgTypes, RRTypes


pyfalog = Logger(__name__)

ProjectedMap = {
    FittingModuleState.OVERHEATED: FittingModuleState.ACTIVE,
    FittingModuleState.ACTIVE: FittingModuleState.OFFLINE,
    FittingModuleState.OFFLINE: FittingModuleState.ACTIVE,
    FittingModuleState.ONLINE: FittingModuleState.ACTIVE  # Just in case
}


# Old state : New State
LocalMap = {
    FittingModuleState.OVERHEATED: FittingModuleState.ACTIVE,
    FittingModuleState.ACTIVE: FittingModuleState.ONLINE,
    FittingModuleState.OFFLINE: FittingModuleState.ONLINE,
    FittingModuleState.ONLINE: FittingModuleState.ACTIVE
}


# For system effects. They should only ever be online or offline
ProjectedSystem = {
    FittingModuleState.OFFLINE: FittingModuleState.ONLINE,
    FittingModuleState.ONLINE: FittingModuleState.OFFLINE
}


class Module(HandledItem, HandledCharge, ItemAttrShortcut, ChargeAttrShortcut, MutatedMixin):
    """An instance of this class represents a module together with its charge and modified attributes"""
    MINING_ATTRIBUTES = ("miningAmount",)
    SYSTEM_GROUPS = (
        "Effect Beacon", "MassiveEnvironments", "Abyssal Hazards",
        "Non-Interactable Object", "Destructible Effect Beacon")

    def __init__(self, item, baseItem=None, mutaplasmid=None):
        """Initialize a module from the program"""

        self.itemID = item.ID if item is not None else None

        self._item = item
        self._mutaInit(baseItem=baseItem, mutaplasmid=mutaplasmid)

        if item is not None and self.isInvalid:
            raise ValueError("Passed item is not a Module")

        self.__charge = None

        self.projected = False
        self.projectionRange = None
        self.state = FittingModuleState.ONLINE
        self.build()

    @reconstructor
    def init(self):
        """Initialize a module from the database and validate"""
        self._item = None
        self.__charge = None

        # we need this early if module is invalid and returns early
        self.__slot = self.dummySlot

        if self.itemID:
            self._item = eos.db.getItem(self.itemID)
            if self._item is None:
                pyfalog.error("Item (id: {0}) does not exist", self.itemID)
                return

        try:
            self._mutaReconstruct()
        except MutaError:
            return

        if self.isInvalid:
            pyfalog.error("Item (id: {0}) is not a Module", self.itemID)
            return

        if self.chargeID:
            self.__charge = eos.db.getItem(self.chargeID)

        self.build()

    def build(self):
        """ Builds internal module variables from both init's """

        if self.__charge and self.__charge.category.name != "Charge":
            self.__charge = None

        self.rahPatternOverride = None

        self.__baseVolley = None
        self.__baseRRAmount = None
        self.__miningYield = None
        self.__miningWaste = None
        self.__reloadTime = None
        self.__reloadForce = None
        self.__chargeCycles = None
        self.__hardpoint = FittingHardpoint.NONE
        self.__itemModifiedAttributes = ModifiedAttributeDict(parent=self)
        self.__chargeModifiedAttributes = ModifiedAttributeDict(parent=self)
        self.__slot = self.dummySlot  # defaults to None

        if self._item:
            self.__itemModifiedAttributes.original = self._item.attributes
            self.__itemModifiedAttributes.overrides = self._item.overrides
            self.__hardpoint = self.__calculateHardpoint(self._item)
            self.__slot = self.calculateSlot(self._item)

            self._mutaLoadMutators(mutatorClass=MutatorModule)
            self.__itemModifiedAttributes.mutators = self.mutators

        if self.__charge:
            self.__chargeModifiedAttributes.original = self.__charge.attributes
            self.__chargeModifiedAttributes.overrides = self.__charge.overrides

    @classmethod
    def buildEmpty(cls, slot):
        empty = Module(None)
        empty.__slot = slot
        empty.dummySlot = slot
        return empty

    @classmethod
    def buildRack(cls, slot, num=None):
        empty = Rack(None)
        empty.__slot = slot
        empty.dummySlot = slot
        empty.num = num
        return empty

    @property
    def isEmpty(self):
        return self.dummySlot is not None

    @property
    def hardpoint(self):
        return self.__hardpoint

    @property
    def isInvalid(self):
        # todo: validate baseItem as well if it's set.
        if self.isEmpty:
            return False
        if self._item is None:
            return True
        if (
            self._item.category.name not in ("Module", "Subsystem", "Structure Module")
            and self._item.group.name not in self.SYSTEM_GROUPS
        ):
            return True
        if (
            self._item.category.name == "Structure Module"
            and self._item.group.name == "Quantum Cores"
        ):
            return True
        if self._mutaIsInvalid:
            return True
        return False

    @property
    def numCharges(self):
        return self.getNumCharges(self.charge)

    def getNumCharges(self, charge):
        if charge is None:
            charges = 0
        else:
            chargeVolume = charge.attributes['volume'].value
            containerCapacity = self.item.attributes['capacity'].value
            if chargeVolume is None or containerCapacity is None:
                charges = 0
            else:
                charges = int(floatUnerr(containerCapacity / chargeVolume))
        return charges

    @property
    def numShots(self):
        if self.charge is None:
            return 0
        if self.__chargeCycles is None and self.charge:
            numCharges = self.numCharges
            # Usual ammo like projectiles and missiles
            if numCharges > 0 and "chargeRate" in self.itemModifiedAttributes:
                self.__chargeCycles = self.__calculateAmmoShots()
            # Frequency crystals (combat and mining lasers)
            elif numCharges > 0 and "crystalsGetDamaged" in self.chargeModifiedAttributes:
                self.__chargeCycles = self.__calculateCrystalShots()
            # Scripts and stuff
            else:
                self.__chargeCycles = 0
            return self.__chargeCycles
        else:
            return self.__chargeCycles

    @property
    def modPosition(self):
        return self.getModPosition()

    def getModPosition(self, fit=None):
        # Pass in fit for reliability. When it's not passed, we rely on owner and owner
        # is set by sqlalchemy during flush
        fit = fit if fit is not None else self.owner
        if fit:
            container = fit.projectedModules if self.isProjected else fit.modules
            try:
                return container.index(self)
            except ValueError:
                return None
        return None

    @property
    def isProjected(self):
        if self.owner:
            return self in self.owner.projectedModules
        return None

    @property
    def isExclusiveSystemEffect(self):
        # See issue #2258
        # return self.item.group.name in ("Effect Beacon", "Non-Interactable Object", "MassiveEnvironments")
        return False

    @property
    def isCapitalSize(self):
        return self.getModifiedItemAttr("volume", 0) >= 4000

    @property
    def hpBeforeReload(self):
        """
        If item is some kind of repairer with charges, calculate
        HP it reps before going into reload.
        """
        cycles = self.numShots
        armorRep = self.getModifiedItemAttr("armorDamageAmount") or 0
        shieldRep = self.getModifiedItemAttr("shieldBonus") or 0
        if not cycles or (not armorRep and not shieldRep):
            return 0
        hp = round((armorRep + shieldRep) * cycles)
        return hp

    def __calculateAmmoShots(self):
        if self.charge is not None:
            # Set number of cycles before reload is needed
            # numcycles = math.floor(module_capacity / (module_volume * module_chargerate))
            chargeRate = self.getModifiedItemAttr("chargeRate")
            numCharges = self.numCharges
            numShots = math.floor(numCharges / chargeRate)
        else:
            numShots = None
        return numShots

    def __calculateCrystalShots(self):
        if self.charge is not None:
            if self.getModifiedChargeAttr("crystalsGetDamaged") == 1:
                # For depletable crystals, calculate average amount of shots before it's destroyed
                hp = self.getModifiedChargeAttr("hp")
                chance = self.getModifiedChargeAttr("crystalVolatilityChance")
                damage = self.getModifiedChargeAttr("crystalVolatilityDamage")
                crystals = self.numCharges
                numShots = math.floor((crystals * hp) / (damage * chance))
            else:
                # Set 0 (infinite) for permanent crystals like t1 laser crystals
                numShots = 0
        else:
            numShots = None
        return numShots

    @property
    def maxRange(self):
        attrs = ("maxRange", "shieldTransferRange", "powerTransferRange",
                 "energyDestabilizationRange", "empFieldRange",
                 "ecmBurstRange", "warpScrambleRange", "cargoScanRange",
                 "shipScanRange", "surveyScanRange")
        maxRange = None
        for attr in attrs:
            maxRange = self.getModifiedItemAttr(attr)
            if maxRange:
                break
        if maxRange:
            if 'burst projector' in self.item.name.lower():
                maxRange -= self.owner.ship.getModifiedItemAttr("radius")
            return maxRange
        missileMaxRangeData = self.missileMaxRangeData
        if missileMaxRangeData is None:
            return None
        lowerRange, higherRange, higherChance = missileMaxRangeData
        maxRange = lowerRange * (1 - higherChance) + higherRange * higherChance
        return maxRange

    @property
    def missileMaxRangeData(self):
        if self.charge is None:
            return None
        try:
            chargeName = self.charge.group.name
        except AttributeError:
            pass
        else:
            if chargeName in ("Scanner Probe", "Survey Probe"):
                return None

        def calculateRange(maxVelocity, mass, agility, flightTime):
            # Source: http://www.eveonline.com/ingameboard.asp?a=topic&threadID=1307419&page=1#15
            # D_m = V_m * (T_m + T_0*[exp(- T_m/T_0)-1])
            accelTime = min(flightTime, mass * agility / 1000000)
            # Average distance done during acceleration
            duringAcceleration = maxVelocity / 2 * accelTime
            # Distance done after being at full speed
            fullSpeed = maxVelocity * (flightTime - accelTime)
            maxRange = duringAcceleration + fullSpeed
            return maxRange

        maxVelocity = self.getModifiedChargeAttr("maxVelocity")
        if not maxVelocity:
            return None
        shipRadius = self.owner.ship.getModifiedItemAttr("radius")
        # Flight time has bonus based on ship radius, see https://github.com/pyfa-org/Pyfa/issues/2083
        flightTime = floatUnerr(self.getModifiedChargeAttr("explosionDelay") / 1000 + shipRadius / maxVelocity)
        mass = self.getModifiedChargeAttr("mass")
        agility = self.getModifiedChargeAttr("agility")
        lowerTime = math.floor(flightTime)
        higherTime = math.ceil(flightTime)
        lowerRange = calculateRange(maxVelocity, mass, agility, lowerTime)
        higherRange = calculateRange(maxVelocity, mass, agility, higherTime)
        # Fof range limit is supposedly calculated based on overview (surface-to-surface) range
        if 'fofMissileLaunching' in self.charge.effects:
            rangeLimit = self.getModifiedChargeAttr("maxFOFTargetRange")
            if rangeLimit:
                lowerRange = min(lowerRange, rangeLimit)
                higherRange = min(higherRange, rangeLimit)
        # Make range center-to-surface, as missiles spawn in the center of the ship
        lowerRange = max(0, lowerRange - shipRadius)
        higherRange = max(0, higherRange - shipRadius)
        higherChance = flightTime - lowerTime
        return lowerRange, higherRange, higherChance

    @property
    def falloff(self):
        attrs = ("falloffEffectiveness", "falloff", "shipScanFalloff")
        for attr in attrs:
            falloff = self.getModifiedItemAttr(attr)
            if falloff:
                return falloff

    @property
    def slot(self):
        return self.__slot

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    @property
    def chargeModifiedAttributes(self):
        return self.__chargeModifiedAttributes

    @property
    def item(self):
        return self._item if self._item != 0 else None

    @property
    def charge(self):
        return self.__charge if self.__charge != 0 else None

    @charge.setter
    def charge(self, charge):
        self.__charge = charge
        if charge is not None:
            self.chargeID = charge.ID
            self.__chargeModifiedAttributes.original = charge.attributes
            self.__chargeModifiedAttributes.overrides = charge.overrides
        else:
            self.chargeID = None
            self.__chargeModifiedAttributes.original = None
            self.__chargeModifiedAttributes.overrides = {}

        self.__itemModifiedAttributes.clear()

    def getMiningYPS(self, ignoreState=False):
        if self.isEmpty:
            return 0
        if not ignoreState and self.state < FittingModuleState.ACTIVE:
            return 0
        if self.__miningYield is None:
            self.__miningYield, self.__miningWaste = self.__calculateMining()
        return self.__miningYield

    def getMiningWPS(self, ignoreState=False):
        if self.isEmpty:
            return 0
        if not ignoreState and self.state < FittingModuleState.ACTIVE:
            return 0
        if self.__miningWaste is None:
            self.__miningYield, self.__miningWaste = self.__calculateMining()
        return self.__miningWaste

    def __calculateMining(self):
        yield_ = self.getModifiedItemAttr("miningAmount")
        if yield_:
            cycleParams = self.getCycleParameters()
            if cycleParams is None:
                yps = 0
            else:
                cycleTime = cycleParams.averageTime
                yps = yield_ / (cycleTime / 1000.0)
        else:
            yps = 0
        wasteChance = self.getModifiedItemAttr("miningWasteProbability")
        wasteMult = self.getModifiedItemAttr("miningWastedVolumeMultiplier")
        wps = yps * max(0, min(1, wasteChance / 100)) * wasteMult
        return yps, wps

    def isDealingDamage(self, ignoreState=False):
        volleyParams = self.getVolleyParameters(ignoreState=ignoreState)
        for volley in volleyParams.values():
            if volley.total > 0:
                return True
        return False

    def canDealDamage(self, ignoreState=False):
        if self.isEmpty:
            return False
        for effect in self.item.effects.values():
            if effect.dealsDamage and (
                ignoreState or
                effect.isType('offline') or
                (effect.isType('passive') and self.state >= FittingModuleState.ONLINE) or
                (effect.isType('active') and self.state >= FittingModuleState.ACTIVE) or
                (effect.isType('overheat') and self.state >= FittingModuleState.OVERHEATED)
            ):
                return True
        return False

    def getVolleyParameters(self, spoolOptions=None, targetProfile=None, ignoreState=False):
        if self.isEmpty or (self.state < FittingModuleState.ACTIVE and not ignoreState):
            return {0: DmgTypes(0, 0, 0, 0)}
        if self.__baseVolley is None:
            self.__baseVolley = {}
            dmgGetter = self.getModifiedChargeAttr if self.charge else self.getModifiedItemAttr
            dmgMult = self.getModifiedItemAttr("damageMultiplier", 1)
            # Some delay attributes have non-0 default value, so we have to pick according to effects
            if {'superWeaponAmarr', 'superWeaponCaldari', 'superWeaponGallente', 'superWeaponMinmatar', 'lightningWeapon'}.intersection(self.item.effects):
                dmgDelay = self.getModifiedItemAttr("damageDelayDuration", 0)
            elif {'doomsdayBeamDOT', 'doomsdaySlash', 'doomsdayConeDOT'}.intersection(self.item.effects):
                dmgDelay = self.getModifiedItemAttr("doomsdayWarningDuration", 0)
            else:
                dmgDelay = 0
            dmgDuration = self.getModifiedItemAttr("doomsdayDamageDuration", 0)
            dmgSubcycle = self.getModifiedItemAttr("doomsdayDamageCycleTime", 0)
            # Reaper DD can damage each target only once
            if dmgDuration != 0 and dmgSubcycle != 0 and 'doomsdaySlash' not in self.item.effects:
                subcycles = math.floor(floatUnerr(dmgDuration / dmgSubcycle))
            else:
                subcycles = 1
            for i in range(subcycles):
                self.__baseVolley[dmgDelay + dmgSubcycle * i] = DmgTypes(
                    em=(dmgGetter("emDamage", 0)) * dmgMult,
                    thermal=(dmgGetter("thermalDamage", 0)) * dmgMult,
                    kinetic=(dmgGetter("kineticDamage", 0)) * dmgMult,
                    explosive=(dmgGetter("explosiveDamage", 0)) * dmgMult)
        spoolType, spoolAmount = resolveSpoolOptions(spoolOptions, self)
        spoolBoost = calculateSpoolup(
            self.getModifiedItemAttr("damageMultiplierBonusMax", 0),
            self.getModifiedItemAttr("damageMultiplierBonusPerCycle", 0),
            self.rawCycleTime / 1000, spoolType, spoolAmount)[0]
        spoolMultiplier = 1 + spoolBoost
        adjustedVolley = {}
        for volleyTime, volleyValue in self.__baseVolley.items():
            adjustedVolley[volleyTime] = DmgTypes(
                em=volleyValue.em * spoolMultiplier * (1 - getattr(targetProfile, "emAmount", 0)),
                thermal=volleyValue.thermal * spoolMultiplier * (1 - getattr(targetProfile, "thermalAmount", 0)),
                kinetic=volleyValue.kinetic * spoolMultiplier * (1 - getattr(targetProfile, "kineticAmount", 0)),
                explosive=volleyValue.explosive * spoolMultiplier * (1 - getattr(targetProfile, "explosiveAmount", 0)))
        return adjustedVolley

    def getVolley(self, spoolOptions=None, targetProfile=None, ignoreState=False):
        volleyParams = self.getVolleyParameters(spoolOptions=spoolOptions, targetProfile=targetProfile, ignoreState=ignoreState)
        if len(volleyParams) == 0:
            return DmgTypes(0, 0, 0, 0)
        return volleyParams[min(volleyParams)]

    def getDps(self, spoolOptions=None, targetProfile=None, ignoreState=False, getSpreadDPS=False):
        dmgDuringCycle = DmgTypes(0, 0, 0, 0)
        cycleParams = self.getCycleParameters()
        if cycleParams is None:
            return dmgDuringCycle
        volleyParams = self.getVolleyParameters(spoolOptions=spoolOptions, targetProfile=targetProfile, ignoreState=ignoreState)
        avgCycleTime = cycleParams.averageTime
        if len(volleyParams) == 0 or avgCycleTime == 0:
            return dmgDuringCycle
        for volleyValue in volleyParams.values():
            dmgDuringCycle += volleyValue
        dpsFactor = 1 / (avgCycleTime / 1000)
        dps = DmgTypes(
            em=dmgDuringCycle.em * dpsFactor,
            thermal=dmgDuringCycle.thermal * dpsFactor,
            kinetic=dmgDuringCycle.kinetic * dpsFactor,
            explosive=dmgDuringCycle.explosive * dpsFactor)
        if not getSpreadDPS:
            return dps
        return {'em':dmgDuringCycle.em * dpsFactor,
                'therm': dmgDuringCycle.thermal * dpsFactor,
                'kin': dmgDuringCycle.kinetic * dpsFactor,
                'exp': dmgDuringCycle.explosive * dpsFactor}

    def isRemoteRepping(self, ignoreState=False):
        repParams = self.getRepAmountParameters(ignoreState=ignoreState)
        for rrData in repParams.values():
            if rrData:
                return True
        return False

    def getRepAmountParameters(self, spoolOptions=None, ignoreState=False):
        if self.isEmpty or (self.state < FittingModuleState.ACTIVE and not ignoreState):
            return {}
        remoteModuleGroups = {
            "Remote Armor Repairer": "Armor",
            "Ancillary Remote Armor Repairer": "Armor",
            "Mutadaptive Remote Armor Repairer": "Armor",
            "Remote Hull Repairer": "Hull",
            "Remote Shield Booster": "Shield",
            "Ancillary Remote Shield Booster": "Shield",
            "Remote Capacitor Transmitter": "Capacitor"}
        rrType = remoteModuleGroups.get(self.item.group.name)
        if rrType is None:
            return {}
        if self.__baseRRAmount is None:
            self.__baseRRAmount = {}
            shieldAmount = 0
            armorAmount = 0
            hullAmount = 0
            capacitorAmount = 0
            if rrType == "Hull":
                hullAmount += self.getModifiedItemAttr("structureDamageAmount", 0)
            elif rrType == "Armor":
                if self.item.group.name == "Ancillary Remote Armor Repairer" and self.charge:
                    mult = self.getModifiedItemAttr("chargedArmorDamageMultiplier", 1)
                else:
                    mult = 1
                armorAmount += self.getModifiedItemAttr("armorDamageAmount", 0) * mult
            elif rrType == "Shield":
                shieldAmount += self.getModifiedItemAttr("shieldBonus", 0)
            elif rrType == "Capacitor":
                capacitorAmount += self.getModifiedItemAttr("powerTransferAmount", 0)
            rrDelay = 0 if rrType == "Shield" else self.rawCycleTime
            self.__baseRRAmount[rrDelay] = RRTypes(shield=shieldAmount, armor=armorAmount, hull=hullAmount, capacitor=capacitorAmount)
        spoolType, spoolAmount = resolveSpoolOptions(spoolOptions, self)
        spoolBoost = calculateSpoolup(
            self.getModifiedItemAttr("repairMultiplierBonusMax", 0),
            self.getModifiedItemAttr("repairMultiplierBonusPerCycle", 0),
            self.rawCycleTime / 1000, spoolType, spoolAmount)[0]
        spoolMultiplier = 1 + spoolBoost
        adjustedRRAmount = {}
        for rrTime, rrAmount in self.__baseRRAmount.items():
            if spoolMultiplier == 1:
                adjustedRRAmount[rrTime] = rrAmount
            else:
                adjustedRRAmount[rrTime] = rrAmount * spoolMultiplier
        return adjustedRRAmount

    def getRemoteReps(self, spoolOptions=None, ignoreState=False, reloadOverride=None):
        rrDuringCycle = RRTypes(0, 0, 0, 0)
        cycleParams = self.getCycleParameters(reloadOverride=reloadOverride)
        if cycleParams is None:
            return rrDuringCycle
        repAmountParams = self.getRepAmountParameters(spoolOptions=spoolOptions, ignoreState=ignoreState)
        avgCycleTime = cycleParams.averageTime
        if len(repAmountParams) == 0 or avgCycleTime == 0:
            return rrDuringCycle
        for rrAmount in repAmountParams.values():
            rrDuringCycle += rrAmount
        rrFactor = 1 / (avgCycleTime / 1000)
        rps = rrDuringCycle * rrFactor
        return rps

    def getSpoolData(self, spoolOptions=None):
        weaponMultMax = self.getModifiedItemAttr("damageMultiplierBonusMax", 0)
        weaponMultPerCycle = self.getModifiedItemAttr("damageMultiplierBonusPerCycle", 0)
        if weaponMultMax and weaponMultPerCycle:
            spoolType, spoolAmount = resolveSpoolOptions(spoolOptions, self)
            _, spoolCycles, spoolTime = calculateSpoolup(
                weaponMultMax, weaponMultPerCycle,
                self.rawCycleTime / 1000, spoolType, spoolAmount)
            return spoolCycles, spoolTime
        rrMultMax = self.getModifiedItemAttr("repairMultiplierBonusMax", 0)
        rrMultPerCycle = self.getModifiedItemAttr("repairMultiplierBonusPerCycle", 0)
        if rrMultMax and rrMultPerCycle:
            spoolType, spoolAmount = resolveSpoolOptions(spoolOptions, self)
            _, spoolCycles, spoolTime = calculateSpoolup(
                rrMultMax, rrMultPerCycle,
                self.rawCycleTime / 1000, spoolType, spoolAmount)
            return spoolCycles, spoolTime
        return 0, 0

    @property
    def reloadTime(self):
        # Get reload time from attrs first, then use
        # custom value specified otherwise (e.g. in effects)
        moduleReloadTime = self.getModifiedItemAttr("reloadTime")
        if moduleReloadTime is None:
            moduleReloadTime = self.__reloadTime
        return moduleReloadTime or 0.0

    @reloadTime.setter
    def reloadTime(self, milliseconds):
        self.__reloadTime = milliseconds

    @property
    def forceReload(self):
        return self.__reloadForce

    @forceReload.setter
    def forceReload(self, type):
        self.__reloadForce = type

    def fits(self, fit, hardpointLimit=True):
        """
        Function that determines if a module can be fit to the ship. We always apply slot restrictions no matter what
        (too many assumptions made on this), however all other fitting restrictions are optional
        """

        slot = self.slot
        if slot is None:
            return False
        if fit.getSlotsFree(slot) <= (0 if self.owner != fit else -1):
            return False

        fits = self.__fitRestrictions(fit, hardpointLimit)

        if not fits and fit.ignoreRestrictions:
            self.restrictionOverridden = True
            fits = True
        elif fits and fit.ignoreRestrictions:
            self.restrictionOverridden = False

        return fits

    def __fitRestrictions(self, fit, hardpointLimit=True):

        if not fit.canFit(self.item):
            return False

        # EVE doesn't let capital modules be fit onto subcapital hulls. Confirmed by CCP Larrikin that this is dictated
        # by the modules volume. See GH issue #1096
        if not isinstance(fit.ship, Citadel) and fit.ship.getModifiedItemAttr("isCapitalSize", 0) != 1 and self.isCapitalSize:
            return False

        # If the mod is a subsystem, don't let two subs in the same slot fit
        if self.slot == FittingSlot.SUBSYSTEM:
            subSlot = self.getModifiedItemAttr("subSystemSlot")
            for mod in fit.modules:
                if mod is self:
                    continue
                if mod.getModifiedItemAttr("subSystemSlot") == subSlot:
                    return False

        # Check rig sizes
        if self.slot == FittingSlot.RIG:
            if self.getModifiedItemAttr("rigSize") != fit.ship.getModifiedItemAttr("rigSize"):
                return False

        # Check max group fitted
        # use raw value, since it seems what EVE uses. Example is FAXes with their capacitor boosters,
        # which have unmodified value of 10, and modified of 1, and you can actually fit multiples
        try:
            max = self.item.attributes.get('maxGroupFitted').value
        except AttributeError:
            pass
        else:
            if max:
                current = 0  # if self.owner != fit else -1  # Disabled, see #1278
                for mod in fit.modules:
                    if (mod.item and mod.item.groupID == self.item.groupID and
                            self.getModPosition(fit) != mod.getModPosition(fit)):
                        current += 1

                if current >= max:
                    return False

        # Check this only if we're told to do so
        if hardpointLimit:
            if fit.getHardpointsFree(self.hardpoint) < (1 if self.owner != fit else 0):
                return False

        return True

    def isValidState(self, state):
        """
        Check if the state is valid for this module, without considering other modules at all
        """
        # Check if we're within bounds
        if state < -1 or state > 2:
            return False
        elif state >= FittingModuleState.ACTIVE and (not self.item.isType("active") or self.getModifiedItemAttr('activationBlocked') > 0):
            return False
        elif state == FittingModuleState.OVERHEATED and not self.item.isType("overheat"):
            return False
        # Some destructible effect beacons contain active effects, hardcap those at online state
        elif state > FittingModuleState.ONLINE and self.slot == FittingSlot.SYSTEM:
            return False
        else:
            return True

    def getMaxState(self, proposedState=None):
        states = sorted((s for s in FittingModuleState if proposedState is None or s <= proposedState), reverse=True)
        for state in states:
            if self.isValidState(state):
                return state

    def canHaveState(self, state=None, projectedOnto=None):
        """
        Check with other modules if there are restrictions that might not allow this module to be activated.
        Returns True if state is allowed, or max state module can have if current state is invalid.
        """
        # If we're going to set module to offline, it should be fine for all cases
        item = self.item
        if state <= FittingModuleState.OFFLINE:
            return True

        # Check if the local module is over it's max limit; if it's not, we're fine
        maxGroupOnline = self.getModifiedItemAttr("maxGroupOnline", None)
        maxGroupActive = self.getModifiedItemAttr("maxGroupActive", None)
        if not maxGroupOnline and not maxGroupActive and projectedOnto is None:
            return True

        # Following is applicable only to local modules, we do not want to limit projected
        if projectedOnto is None:
            currOnline = 0
            currActive = 0
            group = item.group.name
            maxState = None
            for mod in self.owner.modules:
                currItem = getattr(mod, "item", None)
                if currItem is not None and currItem.group.name == group:
                    if mod.state >= FittingModuleState.ONLINE:
                        currOnline += 1
                    if mod.state >= FittingModuleState.ACTIVE:
                        currActive += 1
                    if maxGroupOnline and currOnline > maxGroupOnline:
                        if maxState is None or maxState > FittingModuleState.OFFLINE:
                            maxState = FittingModuleState.OFFLINE
                            break
                    if maxGroupActive and currActive > maxGroupActive:
                        if maxState is None or maxState > FittingModuleState.ONLINE:
                            maxState = FittingModuleState.ONLINE
            return True if maxState is None else maxState
        # For projected, we're checking if ship is vulnerable to given item
        else:
            # Do not allow to apply offensive modules on ship with offensive module immunite, with few exceptions
            # (all effects which apply instant modification are exception, generally speaking)
            if item.offensive and projectedOnto.ship.getModifiedItemAttr("disallowOffensiveModifiers") == 1:
                offensiveNonModifiers = {"energyDestabilizationNew",
                                         "leech",
                                         "energyNosferatuFalloff",
                                         "energyNeutralizerFalloff"}
                if not offensiveNonModifiers.intersection(set(item.effects)):
                    return FittingModuleState.OFFLINE
            # If assistive modules are not allowed, do not let to apply these altogether
            if item.assistive and projectedOnto.ship.getModifiedItemAttr("disallowAssistance") == 1:
                return FittingModuleState.OFFLINE
            return True

    def isValidCharge(self, charge):
        # Check sizes, if 'charge size > module volume' it won't fit
        if charge is None:
            return True
        chargeVolume = charge.attributes['volume'].value
        moduleCapacity = self.item.attributes['capacity'].value
        if chargeVolume is not None and moduleCapacity is not None and chargeVolume > moduleCapacity:
            return False

        itemChargeSize = self.getModifiedItemAttr("chargeSize")
        if itemChargeSize > 0:
            chargeSize = charge.getAttribute('chargeSize')
            if itemChargeSize != chargeSize:
                return False

        chargeGroup = charge.groupID
        for i in range(5):
            itemChargeGroup = self.getModifiedItemAttr('chargeGroup' + str(i), None)
            if not itemChargeGroup:
                continue
            if itemChargeGroup == chargeGroup:
                return True

        return False

    def getValidCharges(self):
        validCharges = set()
        for i in range(5):
            itemChargeGroup = self.getModifiedItemAttr('chargeGroup' + str(i), None)
            if itemChargeGroup:
                g = eos.db.getGroup(int(itemChargeGroup), eager="items.attributes")
                if g is None:
                    continue
                for singleItem in g.items:
                    if singleItem.published and self.isValidCharge(singleItem):
                        validCharges.add(singleItem)

        return validCharges

    @staticmethod
    def __calculateHardpoint(item):
        effectHardpointMap = {
            "turretFitted"  : FittingHardpoint.TURRET,
            "launcherFitted": FittingHardpoint.MISSILE
        }

        if item is None:
            return FittingHardpoint.NONE

        for effectName, slot in effectHardpointMap.items():
            if effectName in item.effects:
                return slot

        return FittingHardpoint.NONE

    @staticmethod
    def calculateSlot(item):
        effectSlotMap = {
            "rigSlot"    : FittingSlot.RIG.value,
            "loPower"    : FittingSlot.LOW.value,
            "medPower"   : FittingSlot.MED.value,
            "hiPower"    : FittingSlot.HIGH.value,
            "subSystem"  : FittingSlot.SUBSYSTEM.value,
            "serviceSlot": FittingSlot.SERVICE.value
        }
        if item is None:
            return None
        for effectName, slot in effectSlotMap.items():
            if effectName in item.effects:
                return slot
        if item.group.name in Module.SYSTEM_GROUPS:
            return FittingSlot.SYSTEM

        return None

    @validates("ID", "itemID", "ammoID")
    def validator(self, key, val):
        map = {
            "ID"    : lambda _val: isinstance(_val, int),
            "itemID": lambda _val: _val is None or isinstance(_val, int),
            "ammoID": lambda _val: isinstance(_val, int)
        }

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def clear(self):
        self.__baseVolley = None
        self.__baseRRAmount = None
        self.__miningYield = None
        self.__miningWaste = None
        self.__reloadTime = None
        self.__reloadForce = None
        self.__chargeCycles = None
        self.itemModifiedAttributes.clear()
        self.chargeModifiedAttributes.clear()

    def calculateModifiedAttributes(self, fit, runTime, forceProjected=False, gang=False, forcedProjRange=DEFAULT):
        # We will run the effect when two conditions are met:
        # 1: It makes sense to run the effect
        #    The effect is either offline
        #    or the effect is passive and the module is in the online state (or higher)

        #    or the effect is active and the module is in the active state (or higher)
        #    or the effect is overheat and the module is in the overheated state (or higher)
        # 2: the runtimes match

        if self.projected or forceProjected:
            context = "projected", "module"
            projected = True
        else:
            context = ("module",)
            projected = False

        projectionRange = self.projectionRange if forcedProjRange is DEFAULT else forcedProjRange

        if self.charge is not None:
            # fix for #82 and it's regression #106
            if not projected or (self.projected and not forceProjected) or gang:
                for effect in self.charge.effects.values():
                    if (
                        effect.runTime == runTime and
                        effect.activeByDefault and (
                            effect.isType("offline") or
                            (effect.isType("passive") and self.state >= FittingModuleState.ONLINE) or
                            (effect.isType("active") and self.state >= FittingModuleState.ACTIVE)) and
                        (not gang or (gang and effect.isType("gang")))
                    ):
                        contexts = ("moduleCharge",)
                        effect.handler(fit, self, contexts, projectionRange, effect=effect)

        if self.item:
            if self.state >= FittingModuleState.OVERHEATED:
                for effect in self.item.effects.values():
                    if effect.runTime == runTime and \
                            effect.isType("overheat") \
                            and not forceProjected \
                            and effect.activeByDefault \
                            and ((gang and effect.isType("gang")) or not gang):
                        effect.handler(fit, self, context, projectionRange, effect=effect)

            for effect in self.item.effects.values():
                if effect.runTime == runTime and \
                        effect.activeByDefault and \
                        (effect.isType("offline") or
                         (effect.isType("passive") and self.state >= FittingModuleState.ONLINE) or
                         (effect.isType("active") and self.state >= FittingModuleState.ACTIVE)) \
                        and ((projected and effect.isType("projected")) or not projected) \
                        and ((gang and effect.isType("gang")) or not gang):
                    effect.handler(fit, self, context, projectionRange, effect=effect)

    def getCycleParameters(self, reloadOverride=None):
        """Copied from new eos as well"""
        # Determine if we'll take into account reload time or not
        if reloadOverride is not None:
            factorReload = reloadOverride
        else:
            factorReload = self.owner.factorReload if self.forceReload is None else self.forceReload

        cycles_until_reload = self.numShots
        if cycles_until_reload == 0:
            cycles_until_reload = math.inf

        active_time = self.rawCycleTime
        if active_time == 0:
            return None
        forced_inactive_time = self.reactivationDelay
        reload_time = self.reloadTime
        # Effects which cannot be reloaded have the same processing whether
        # caller wants to take reload time into account or not
        if reload_time is None and cycles_until_reload < math.inf:
            final_cycles = 1
            early_cycles = cycles_until_reload - final_cycles
            # Single cycle until effect cannot run anymore
            if early_cycles == 0:
                return CycleInfo(active_time, 0, 1, False)
            # Multiple cycles with the same parameters
            if forced_inactive_time == 0:
                return CycleInfo(active_time, 0, cycles_until_reload, False)
            # Multiple cycles with different parameters
            return CycleSequence((
                CycleInfo(active_time, forced_inactive_time, early_cycles, False),
                CycleInfo(active_time, 0, final_cycles, False)
            ), 1)
        # Module cycles the same way all the time in 3 cases:
        # 1) caller doesn't want to take into account reload time
        # 2) effect does not have to reload anything to keep running
        # 3) effect has enough time to reload during inactivity periods
        if (
            not factorReload or
            cycles_until_reload == math.inf or
            forced_inactive_time >= reload_time
        ):
            isInactivityReload = factorReload and forced_inactive_time >= reload_time
            return CycleInfo(active_time, forced_inactive_time, math.inf, isInactivityReload)
        # We've got to take reload into consideration
        else:
            final_cycles = 1
            early_cycles = cycles_until_reload - final_cycles
            # If effect has to reload after each its cycle, then its parameters
            # are the same all the time
            if early_cycles == 0:
                return CycleInfo(active_time, reload_time, math.inf, True)
            return CycleSequence((
                CycleInfo(active_time, forced_inactive_time, early_cycles, False),
                CycleInfo(active_time, reload_time, final_cycles, True)
            ), math.inf)

    @property
    def rawCycleTime(self):
        speed = max(
                self.getModifiedItemAttr("speed", 0),  # Most weapons
                self.getModifiedItemAttr("duration", 0),  # Most average modules
                self.getModifiedItemAttr("durationHighisGood", 0),  # Most average modules
                self.getModifiedItemAttr("durationSensorDampeningBurstProjector", 0),
                self.getModifiedItemAttr("durationTargetIlluminationBurstProjector", 0),
                self.getModifiedItemAttr("durationECMJammerBurstProjector", 0),
                self.getModifiedItemAttr("durationWeaponDisruptionBurstProjector", 0)
        )
        return speed

    @property
    def disallowRepeatingAction(self):
        return self.getModifiedItemAttr("disallowRepeatingActivation", 0)

    @property
    def reactivationDelay(self):
        return self.getModifiedItemAttr("moduleReactivationDelay", 0)

    @property
    def capUse(self):
        capNeed = self.getModifiedItemAttr("capacitorNeed")
        if capNeed and self.state >= FittingModuleState.ACTIVE:
            cycleParams = self.getCycleParameters()
            if cycleParams is None:
                return 0
            cycleTime = cycleParams.averageTime
            if cycleTime > 0:
                capUsed = capNeed / (cycleTime / 1000.0)
                return capUsed
        else:
            return 0

    @staticmethod
    def getProposedState(mod, click, proposedState=None):
        pyfalog.debug("Get proposed state for module.")
        if mod.slot == FittingSlot.SUBSYSTEM or mod.isEmpty:
            return FittingModuleState.ONLINE

        if mod.slot == FittingSlot.SYSTEM:
            transitionMap = ProjectedSystem
        else:
            transitionMap = ProjectedMap if mod.projected else LocalMap

        currState = mod.state

        if proposedState is not None:
            state = proposedState
        elif click == "right":
            state = FittingModuleState.OVERHEATED
        elif click == "ctrl":
            state = FittingModuleState.OFFLINE
        else:
            try:
                state = transitionMap[currState]
            except KeyError:
                state = min(transitionMap)
            # If passive module tries to transition into online and fails,
            # put it to passive instead
            if not mod.isValidState(state) and currState == FittingModuleState.ONLINE:
                state = FittingModuleState.OFFLINE

        return mod.getMaxState(proposedState=state)

    def __deepcopy__(self, memo):
        item = self.item
        if item is None:
            copy = Module.buildEmpty(self.slot)
        else:
            copy = Module(self.item, self.baseItem, self.mutaplasmid)
        copy.charge = self.charge
        copy.state = self.state
        copy.spoolType = self.spoolType
        copy.spoolAmount = self.spoolAmount
        copy.projectionRange = self.projectionRange
        copy.rahPatternOverride = self.rahPatternOverride
        self._mutaApplyMutators(mutatorClass=MutatorModule, targetInstance=copy)

        return copy

    def rebase(self, item):
        state = self.state
        charge = self.charge
        spoolType = self.spoolType
        spoolAmount = self.spoolAmount
        projectionRange = self.projectionRange
        rahPatternOverride = self.rahPatternOverride

        Module.__init__(self, item, self.baseItem, self.mutaplasmid)
        self.state = state
        if self.isValidCharge(charge):
            self.charge = charge
        self.spoolType = spoolType
        self.spoolAmount = spoolAmount
        self.projectionRange = projectionRange
        self.rahPatternOverride = rahPatternOverride
        self._mutaApplyMutators(mutatorClass=MutatorModule)

    def __repr__(self):
        if self.item:
            return "Module(ID={}, name={}) at {}".format(self.item.ID, self.item.name, hex(id(self)))
        else:
            return "EmptyModule() at {}".format(hex(id(self)))


class Rack(Module):
    """
    This is simply the Module class named something else to differentiate
    it for app logic. The only thing interesting about it is the num property,
    which is the number of slots for this rack
    """
    num = None
