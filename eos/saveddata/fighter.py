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

from logbook import Logger

from sqlalchemy.orm import validates, reconstructor

import eos.db
from eos.effectHandlerHelpers import HandledItem, HandledCharge
from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut, ChargeAttrShortcut
from eos.saveddata.fighterAbility import FighterAbility
from eos.utils.stats import DmgTypes
from eos.const import FittingSlot

pyfalog = Logger(__name__)


class Fighter(HandledItem, HandledCharge, ItemAttrShortcut, ChargeAttrShortcut):
    DAMAGE_TYPES = ("em", "kinetic", "explosive", "thermal")
    DAMAGE_TYPES2 = ("EM", "Kin", "Exp", "Therm")

    def __init__(self, item):
        """Initialize a fighter from the program"""
        self.__item = item

        if self.isInvalid:
            raise ValueError("Passed item is not a Fighter")

        self.itemID = item.ID if item is not None else None
        self.projected = False
        self.active = True

        # -1 is a placeholder that represents max squadron size, which we may not know yet as ships may modify this with
        # their effects. If user changes this, it is then overridden with user value.
        self.amount = -1

        self.__abilities = self.__getAbilities()

        self.build()

        standardAttackActive = False
        for ability in self.abilities:
            if ability.effect.isImplemented and ability.effect.handlerName == 'fighterabilityattackm':
                # Activate "standard attack" if available
                ability.active = True
                standardAttackActive = True
            else:
                # Activate all other abilities (Neut, Web, etc) except propmods if no standard attack is active
                if ability.effect.isImplemented and \
                                standardAttackActive is False and \
                                ability.effect.handlerName != 'fighterabilitymicrowarpdrive' and \
                                ability.effect.handlerName != 'fighterabilityevasivemaneuvers':
                    ability.active = True

    @reconstructor
    def init(self):
        """Initialize a fighter from the database and validate"""
        self.__item = None

        if self.itemID:
            self.__item = eos.db.getItem(self.itemID)
            if self.__item is None:
                pyfalog.error("Item (id: {0}) does not exist", self.itemID)
                return

        if self.isInvalid:
            pyfalog.error("Item (id: {0}) is not a Fighter", self.itemID)
            return

        self.build()

    def build(self):
        """ Build object. Assumes proper and valid item already set """
        self.__charge = None
        self.__baseVolley = None
        self.__miningyield = None
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__chargeModifiedAttributes = ModifiedAttributeDict()

        if len(self.abilities) != len(self.item.effects):
            self.__abilities = []
            for ability in self.__getAbilities():
                self.__abilities.append(ability)

        if self.__item:
            self.__itemModifiedAttributes.original = self.__item.attributes
            self.__itemModifiedAttributes.overrides = self.__item.overrides
            self.__slot = self.__calculateSlot(self.__item)

            chargeID = self.getModifiedItemAttr("fighterAbilityLaunchBombType")
            if chargeID:
                charge = eos.db.getItem(int(chargeID))
                self.__charge = charge
                self.__chargeModifiedAttributes.original = charge.attributes
                self.__chargeModifiedAttributes.overrides = charge.overrides

    def __getAbilities(self):
        """Returns list of FighterAbilities that are loaded with data"""
        return [FighterAbility(effect) for effect in list(self.item.effects.values())]

    def __calculateSlot(self, item):
        types = {
            "Light"  : FittingSlot.F_LIGHT,
            "Support": FittingSlot.F_SUPPORT,
            "Heavy"  : FittingSlot.F_HEAVY,
            "StandupLight": FittingSlot.FS_LIGHT,
            "StandupSupport": FittingSlot.FS_SUPPORT,
            "StandupHeavy": FittingSlot.FS_HEAVY
        }

        for t, slot in types.items():
            if self.getModifiedItemAttr("fighterSquadronIs{}".format(t)):
                return slot

    @property
    def slot(self):
        return self.__slot

    @property
    def amountActive(self):
        return int(self.getModifiedItemAttr("fighterSquadronMaxSize")) if self.amount == -1 else self.amount

    @amountActive.setter
    def amountActive(self, i):
        self.amount = int(max(min(i, self.getModifiedItemAttr("fighterSquadronMaxSize")), 0))

    @property
    def fighterSquadronMaxSize(self):
        return int(self.getModifiedItemAttr("fighterSquadronMaxSize"))

    @property
    def abilities(self):
        return self.__abilities or []

    @property
    def charge(self):
        return self.__charge

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    @property
    def chargeModifiedAttributes(self):
        return self.__chargeModifiedAttributes

    @property
    def isInvalid(self):
        return self.__item is None or self.__item.category.name != "Fighter"

    @property
    def item(self):
        return self.__item

    @property
    def hasAmmo(self):
        return self.charge is not None

    def getVolley(self, targetResists=None):
        if not self.active or self.amountActive <= 0:
            return DmgTypes(0, 0, 0, 0)
        if self.__baseVolley is None:
            em = 0
            therm = 0
            kin = 0
            exp = 0
            for ability in self.abilities:
                # Not passing resists here as we want to calculate and store base volley
                abilityVolley = ability.getVolley()
                em += abilityVolley.em
                therm += abilityVolley.thermal
                kin += abilityVolley.kinetic
                exp += abilityVolley.explosive
            self.__baseVolley = DmgTypes(em, therm, kin, exp)
        volley = DmgTypes(
            em=self.__baseVolley.em * (1 - getattr(targetResists, "emAmount", 0)),
            thermal=self.__baseVolley.thermal * (1 - getattr(targetResists, "thermalAmount", 0)),
            kinetic=self.__baseVolley.kinetic * (1 - getattr(targetResists, "kineticAmount", 0)),
            explosive=self.__baseVolley.explosive * (1 - getattr(targetResists, "explosiveAmount", 0)))
        return volley

    def getDps(self, targetResists=None):
        if not self.active or self.amountActive <= 0:
            return DmgTypes(0, 0, 0, 0)
        # Analyze cooldowns when reload is factored in
        if self.owner.factorReload:
            activeTimes = []
            reloadTimes = []
            peakEm = 0
            peakTherm = 0
            peakKin = 0
            peakExp = 0
            steadyEm = 0
            steadyTherm = 0
            steadyKin = 0
            steadyExp = 0
            for ability in self.abilities:
                abilityDps = ability.getDps(targetResists=targetResists)
                # Peak dps
                peakEm += abilityDps.em
                peakTherm += abilityDps.thermal
                peakKin += abilityDps.kinetic
                peakExp += abilityDps.explosive
                # Infinite use - add to steady dps
                if ability.numShots == 0:
                    steadyEm += abilityDps.em
                    steadyTherm += abilityDps.thermal
                    steadyKin += abilityDps.kinetic
                    steadyExp += abilityDps.explosive
                else:
                    activeTimes.append(ability.numShots * ability.cycleTime)
                    reloadTimes.append(ability.reloadTime)
            steadyDps = DmgTypes(steadyEm, steadyTherm, steadyKin, steadyExp)
            if len(activeTimes) > 0:
                shortestActive = sorted(activeTimes)[0]
                longestReload = sorted(reloadTimes, reverse=True)[0]
                peakDps = DmgTypes(peakEm, peakTherm, peakKin, peakExp)
                peakAdjustFactor = shortestActive / (shortestActive + longestReload)
                peakDpsAdjusted = DmgTypes(
                    em=peakDps.em * peakAdjustFactor,
                    thermal=peakDps.thermal * peakAdjustFactor,
                    kinetic=peakDps.kinetic * peakAdjustFactor,
                    explosive=peakDps.explosive * peakAdjustFactor)
                dps = max(steadyDps, peakDpsAdjusted, key=lambda d: d.total)
                return dps
            else:
                return steadyDps
        # Just sum all abilities when not taking reload into consideration
        else:
            em = 0
            therm = 0
            kin = 0
            exp = 0
            for ability in self.abilities:
                abilityDps = ability.getDps(targetResists=targetResists)
                em += abilityDps.em
                therm += abilityDps.thermal
                kin += abilityDps.kinetic
                exp += abilityDps.explosive
            return DmgTypes(em, therm, kin, exp)

    @property
    def maxRange(self):
        attrs = ("shieldTransferRange", "powerTransferRange",
                 "energyDestabilizationRange", "empFieldRange",
                 "ecmBurstRange", "maxRange")
        for attr in attrs:
            maxRange = self.getModifiedItemAttr(attr, None)
            if maxRange is not None:
                return maxRange
        if self.charge is not None:
            delay = self.getModifiedChargeAttr("explosionDelay", None)
            speed = self.getModifiedChargeAttr("maxVelocity", None)
            if delay is not None and speed is not None:
                return delay / 1000.0 * speed

    # Had to add this to match the falloff property in modules.py
    # Fscking ship scanners. If you find any other falloff attributes,
    # Put them in the attrs tuple.
    @property
    def falloff(self):
        attrs = ("falloff", "falloffEffectiveness")
        for attr in attrs:
            falloff = self.getModifiedItemAttr(attr, None)
            if falloff is not None:
                return falloff

    @validates("ID", "itemID", "chargeID", "amount", "amountActive")
    def validator(self, key, val):
        map = {
            "ID"      : lambda _val: isinstance(_val, int),
            "itemID"  : lambda _val: isinstance(_val, int),
            "chargeID": lambda _val: isinstance(_val, int),
            "amount"  : lambda _val: isinstance(_val, int) and _val >= -1,
        }

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def clear(self):
        self.__baseVolley = None
        self.__miningyield = None
        self.itemModifiedAttributes.clear()
        self.chargeModifiedAttributes.clear()
        [x.clear() for x in self.abilities]

    def canBeApplied(self, projectedOnto):
        """Check if fighter can engage specific fitting"""
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

    def calculateModifiedAttributes(self, fit, runTime, forceProjected=False):
        if not self.active:
            return

        if self.projected or forceProjected:
            context = "projected", "fighter"
            projected = True
        else:
            context = ("fighter",)
            projected = False

        for ability in self.abilities:
            if not ability.active:
                continue

            effect = ability.effect
            if effect.runTime == runTime and effect.activeByDefault and \
                    ((projected and effect.isType("projected")) or not projected):
                if ability.grouped:
                    effect.handler(fit, self, context)
                else:
                    i = 0
                    while i != self.amountActive:
                        effect.handler(fit, self, context)
                        i += 1

    def __deepcopy__(self, memo):
        copy = Fighter(self.item)
        copy.amount = self.amount
        copy.active = self.active
        for ability in self.abilities:
            copyAbility = next(filter(lambda a: a.effectID == ability.effectID, copy.abilities))
            copyAbility.active = ability.active
        return copy

    def fits(self, fit):
        # If ships doesn't support this type of fighter, don't add it
        if fit.getNumSlots(self.slot) == 0:
            return False

        return True
