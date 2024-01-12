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
from eos.effectHandlerHelpers import HandledCharge, HandledItem
from eos.modifiedAttributeDict import ChargeAttrShortcut, ItemAttrShortcut, ModifiedAttributeDict
from eos.saveddata.mutatedMixin import MutatedMixin, MutaError
from eos.saveddata.mutator import MutatorDrone
from eos.utils.cycles import CycleInfo
from eos.utils.default import DEFAULT
from eos.utils.stats import DmgTypes, RRTypes


pyfalog = Logger(__name__)


class Drone(HandledItem, HandledCharge, ItemAttrShortcut, ChargeAttrShortcut, MutatedMixin):
    MINING_ATTRIBUTES = ("miningAmount",)

    def __init__(self, item, baseItem=None, mutaplasmid=None):
        """Initialize a drone from the program"""
        self._item = item
        self._mutaInit(baseItem=baseItem, mutaplasmid=mutaplasmid)

        if self.isInvalid:
            raise ValueError("Passed item is not a Drone")

        self.itemID = item.ID if item is not None else None
        self.amount = 0
        self.amountActive = 0
        self.projected = False
        self.projectionRange = None
        self.build()

    @reconstructor
    def init(self):
        """Initialize a drone from the database and validate"""
        self._item = None

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
            pyfalog.error("Item (id: {0}) is not a Drone", self.itemID)
            return

        self.build()

    def build(self):
        """ Build object. Assumes proper and valid item already set """
        self.__charge = None
        self.__baseVolley = None
        self.__baseRRAmount = None
        self.__miningYield = None
        self.__miningWaste = None
        self.__ehp = None
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self._item.attributes
        self.__itemModifiedAttributes.overrides = self._item.overrides
        self.__chargeModifiedAttributes = ModifiedAttributeDict()

        self._mutaLoadMutators(mutatorClass=MutatorDrone)
        self.__itemModifiedAttributes.mutators = self.mutators

        chargeID = self.getModifiedItemAttr("entityMissileTypeID", None)
        if chargeID:
            charge = eos.db.getItem(int(chargeID))
            self.__charge = charge
            self.__chargeModifiedAttributes.original = charge.attributes
            self.__chargeModifiedAttributes.overrides = charge.overrides

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    @property
    def chargeModifiedAttributes(self):
        return self.__chargeModifiedAttributes

    @property
    def isInvalid(self):
        if self._item is None:
            return True
        if self._item.category.name != "Drone":
            return True
        if self._mutaIsInvalid:
            return True
        return False

    @property
    def item(self):
        return self._item

    @property
    def charge(self):
        return self.__charge

    @property
    def cycleTime(self):
        if self.hasAmmo:
            cycleTime = self.getModifiedItemAttr("missileLaunchDuration", 0)
        else:
            for attr in ("speed", "duration", "durationHighisGood"):
                cycleTime = self.getModifiedItemAttr(attr)
                if cycleTime:
                    break
        if cycleTime is None:
            return 0
        return max(cycleTime, 0)

    @property
    def dealsDamage(self):
        for attr in ("emDamage", "kineticDamage", "explosiveDamage", "thermalDamage"):
            if attr in self.itemModifiedAttributes or attr in self.chargeModifiedAttributes:
                return True

    @property
    def mines(self):
        if "miningAmount" in self.itemModifiedAttributes:
            return True

    @property
    def hasAmmo(self):
        return self.charge is not None

    def isDealingDamage(self):
        volleyParams = self.getVolleyParameters()
        for volley in volleyParams.values():
            if volley.total > 0:
                return True
        return False

    def getVolleyParameters(self, targetProfile=None):
        if not self.dealsDamage or self.amountActive <= 0:
            return {0: DmgTypes(0, 0, 0, 0)}
        if self.__baseVolley is None:
            dmgGetter = self.getModifiedChargeAttr if self.hasAmmo else self.getModifiedItemAttr
            dmgMult = self.amountActive * (self.getModifiedItemAttr("damageMultiplier", 1))
            self.__baseVolley = DmgTypes(
                em=(dmgGetter("emDamage", 0)) * dmgMult,
                thermal=(dmgGetter("thermalDamage", 0)) * dmgMult,
                kinetic=(dmgGetter("kineticDamage", 0)) * dmgMult,
                explosive=(dmgGetter("explosiveDamage", 0)) * dmgMult)
        volley = DmgTypes(
            em=self.__baseVolley.em * (1 - getattr(targetProfile, "emAmount", 0)),
            thermal=self.__baseVolley.thermal * (1 - getattr(targetProfile, "thermalAmount", 0)),
            kinetic=self.__baseVolley.kinetic * (1 - getattr(targetProfile, "kineticAmount", 0)),
            explosive=self.__baseVolley.explosive * (1 - getattr(targetProfile, "explosiveAmount", 0)))
        return {0: volley}

    def getVolley(self, targetProfile=None):
        return self.getVolleyParameters(targetProfile=targetProfile)[0]

    def getDps(self, targetProfile=None):
        volley = self.getVolley(targetProfile=targetProfile)
        if not volley:
            return DmgTypes(0, 0, 0, 0)
        cycleParams = self.getCycleParameters()
        if cycleParams is None:
            return DmgTypes(0, 0, 0, 0)
        dpsFactor = 1 / (cycleParams.averageTime / 1000)
        dps = DmgTypes(
            em=volley.em * dpsFactor,
            thermal=volley.thermal * dpsFactor,
            kinetic=volley.kinetic * dpsFactor,
            explosive=volley.explosive * dpsFactor)
        return dps

    def isRemoteRepping(self, ignoreState=False):
        repParams = self.getRepAmountParameters(ignoreState=ignoreState)
        for rrData in repParams.values():
            if rrData:
                return True
        return False

    def getRepAmountParameters(self, ignoreState=False):
        amount = self.amount if ignoreState else self.amountActive
        if amount <= 0:
            return {}
        if self.__baseRRAmount is None:
            self.__baseRRAmount = {}
            hullAmount = self.getModifiedItemAttr("structureDamageAmount", 0)
            armorAmount = self.getModifiedItemAttr("armorDamageAmount", 0)
            shieldAmount = self.getModifiedItemAttr("shieldBonus", 0)
            if shieldAmount:
                self.__baseRRAmount[0] = RRTypes(
                    shield=shieldAmount * amount,
                    armor=0, hull=0, capacitor=0)
            if armorAmount or hullAmount:
                self.__baseRRAmount[self.cycleTime] = RRTypes(
                    shield=0, armor=armorAmount * amount,
                    hull=hullAmount * amount, capacitor=0)
        return self.__baseRRAmount

    def getRemoteReps(self, ignoreState=False):
        rrDuringCycle = RRTypes(0, 0, 0, 0)
        cycleParams = self.getCycleParameters()
        if cycleParams is None:
            return rrDuringCycle
        repAmountParams = self.getRepAmountParameters(ignoreState=ignoreState)
        avgCycleTime = cycleParams.averageTime
        if len(repAmountParams) == 0 or avgCycleTime == 0:
            return rrDuringCycle
        for rrAmount in repAmountParams.values():
            rrDuringCycle += rrAmount
        rrFactor = 1 / (avgCycleTime / 1000)
        rrDuringCycle *= rrFactor
        return rrDuringCycle

    def getCycleParameters(self, reloadOverride=None):
        cycleTime = self.cycleTime
        if not cycleTime:
            return None
        return CycleInfo(self.cycleTime, 0, math.inf, False)

    def getMiningYPS(self, ignoreState=False):
        if not ignoreState and self.amountActive <= 0:
            return 0
        if self.__miningYield is None:
            self.__miningYield, self.__miningWaste = self.__calculateMining()
        return self.__miningYield

    def getMiningWPS(self, ignoreState=False):
        if not ignoreState and self.amountActive <= 0:
            return 0
        if self.__miningWaste is None:
            self.__miningYield, self.__miningWaste = self.__calculateMining()
        return self.__miningWaste

    def __calculateMining(self):
        if self.mines is True:
            getter = self.getModifiedItemAttr
            cycleParams = self.getCycleParameters()
            if cycleParams is None:
                yps = 0
            else:
                cycleTime = cycleParams.averageTime
                yield_ = sum([getter(d) for d in self.MINING_ATTRIBUTES]) * self.amount
                yps = yield_ / (cycleTime / 1000.0)
            wasteChance = self.getModifiedItemAttr("miningWasteProbability")
            wasteMult = self.getModifiedItemAttr("miningWastedVolumeMultiplier")
            wps = yps * max(0, min(1, wasteChance / 100)) * wasteMult
            return yps, wps
        else:
            return 0, 0

    @property
    def maxRange(self):
        attrs = ("shieldTransferRange", "powerTransferRange",
                 "energyDestabilizationRange", "empFieldRange",
                 "ecmBurstRange", "maxRange", "ECMRangeOptimal")
        for attr in attrs:
            maxRange = self.getModifiedItemAttr(attr)
            if maxRange:
                return maxRange
        if self.charge is not None:
            delay = self.getModifiedChargeAttr("explosionDelay")
            speed = self.getModifiedChargeAttr("maxVelocity")
            if delay is not None and speed is not None:
                return delay / 1000.0 * speed

    @property
    def hp(self):
        hp = {}
        for (type, attr) in (('shield', 'shieldCapacity'), ('armor', 'armorHP'), ('hull', 'hp')):
            hp[type] = self.getModifiedItemAttr(attr)

        return hp

    @property
    def ehp(self):
        if self.__ehp is None:
            if self.owner is None or self.owner.damagePattern is None:
                ehp = self.hp
            else:
                ehp = self.owner.damagePattern.calculateEhp(self)
            self.__ehp = ehp
        return self.__ehp

    def calculateShieldRecharge(self):
        capacity = self.getModifiedItemAttr("shieldCapacity")
        rechargeRate = self.getModifiedItemAttr("shieldRechargeRate") / 1000.0
        return 10 / rechargeRate * math.sqrt(0.25) * (1 - math.sqrt(0.25)) * capacity

    # Had to add this to match the falloff property in modules.py
    # Fscking ship scanners. If you find any other falloff attributes,
    # Put them in the attrs tuple.
    @property
    def falloff(self):
        attrs = ("falloff", "falloffEffectiveness")
        for attr in attrs:
            falloff = self.getModifiedItemAttr(attr)
            if falloff:
                return falloff

    @validates("ID", "itemID", "chargeID", "amount", "amountActive")
    def validator(self, key, val):
        map = {
            "ID"          : lambda _val: isinstance(_val, int),
            "itemID"      : lambda _val: isinstance(_val, int),
            "chargeID"    : lambda _val: isinstance(_val, int),
            "amount"      : lambda _val: isinstance(_val, int) and _val >= 0,
            "amountActive": lambda _val: isinstance(_val, int) and self.amount >= _val >= 0
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
        self.__ehp = None
        self.itemModifiedAttributes.clear()
        self.chargeModifiedAttributes.clear()

    def canBeApplied(self, projectedOnto):
        """Check if drone can engage specific fitting"""
        item = self.item
        # Do not allow to apply offensive modules on ship with offensive module immunite, with few exceptions
        # (all effects which apply instant modification are exception, generally speaking)
        if item.offensive and projectedOnto.ship.getModifiedItemAttr("disallowOffensiveModifiers") == 1:
            offensiveNonModifiers = {"energyDestabilizationNew",
                                     "leech",
                                     "energyNosferatuFalloff",
                                     "energyNeutralizerFalloff"}
            if not offensiveNonModifiers.intersection(set(item.effects)):
                return False
        # If assistive modules are not allowed, do not let to apply these altogether
        if item.assistive and projectedOnto.ship.getModifiedItemAttr("disallowAssistance") == 1:
            return False
        else:
            return True

    def calculateModifiedAttributes(self, fit, runTime, forceProjected=False, forcedProjRange=DEFAULT):
        if self.projected or forceProjected:
            context = "projected", "drone"
            projected = True
        else:
            context = ("drone",)
            projected = False

        projectionRange = self.projectionRange if forcedProjRange is DEFAULT else forcedProjRange

        for effect in self.item.effects.values():
            if effect.runTime == runTime and \
                    effect.activeByDefault and \
                    ((projected is True and effect.isType("projected")) or
                                 projected is False and effect.isType("passive")):
                # See GH issue #765
                if effect.getattr('grouped'):
                    effect.handler(fit, self, context, projectionRange, effect=effect)
                else:
                    i = 0
                    while i != self.amountActive:
                        effect.handler(fit, self, context, projectionRange, effect=effect)
                        i += 1

        if self.charge:
            for effect in self.charge.effects.values():
                if effect.runTime == runTime and effect.activeByDefault:
                    effect.handler(fit, self, ("droneCharge",), projectionRange, effect=effect)

    def __deepcopy__(self, memo):
        copy = Drone(self.item, self.baseItem, self.mutaplasmid)
        copy.amount = self.amount
        copy.amountActive = self.amountActive
        copy.projectionRange = self.projectionRange
        self._mutaApplyMutators(mutatorClass=MutatorDrone, targetInstance=copy)
        return copy

    def rebase(self, item):
        amount = self.amount
        amountActive = self.amountActive
        projectionRange = self.projectionRange

        Drone.__init__(self, item, self.baseItem, self.mutaplasmid)
        self.amount = amount
        self.amountActive = amountActive
        self.projectionRange = projectionRange
        self._mutaApplyMutators(mutatorClass=MutatorDrone)

    def fits(self, fit):
        fitDroneGroupLimits = set()
        for i in range(1, 3):
            groneGrp = fit.ship.getModifiedItemAttr("allowedDroneGroup%d" % i)
            if groneGrp:
                fitDroneGroupLimits.add(int(groneGrp))
        if len(fitDroneGroupLimits) == 0:
            return True
        if self.item.groupID in fitDroneGroupLimits:
            return True
        return False

    def canDealDamage(self, ignoreState=False):
        if self.item is None:
            return False
        for effect in self.item.effects.values():
            if effect.dealsDamage and (ignoreState or self.amountActive > 0):
                return True
        return False
