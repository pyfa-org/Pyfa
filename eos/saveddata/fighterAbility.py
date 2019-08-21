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

from sqlalchemy.orm import reconstructor

from eos.utils.stats import DmgTypes

pyfalog = Logger(__name__)


class FighterAbility:

    # We aren't able to get data on the charges that can be stored with fighters. So we hardcode that data here, keyed
    # with the fighter squadron role
    NUM_SHOTS_MAPPING = {
        1: 0,  # Superiority fighter / Attack
        2: 12,  # Light fighter / Attack
        4: 6,  # Heavy fighter / Heavy attack
        5: 3,  # Heavy fighter / Long range attack
    }
    # Same as above
    REARM_TIME_MAPPING = {
        1: 0,  # Superiority fighter / Attack
        2: 4000,  # Light fighter / Attack
        4: 6000,  # Heavy fighter / Heavy attack
        5: 20000,  # Heavy fighter / Long range attack
    }

    def __init__(self, effect):
        """Initialize from the program"""
        self.__effect = effect
        self.effectID = effect.ID if effect is not None else None
        self.active = False
        self.build()

    @reconstructor
    def init(self):
        """Initialize from the database"""
        self.__effect = None

        if self.effectID:
            self.__effect = next((x for x in self.fighter.item.effects.values() if x.ID == self.effectID), None)
            if self.__effect is None:
                pyfalog.error("Effect (id: {0}) does not exist", self.effectID)
                return

        self.build()

    def build(self):
        pass

    @property
    def effect(self):
        return self.__effect

    @property
    def name(self):
        return self.__effect.getattr('displayName') or self.__effect.name

    @property
    def attrPrefix(self):
        return self.__effect.getattr('prefix')

    @property
    def dealsDamage(self):
        attr = "{}DamageMultiplier".format(self.attrPrefix)
        return attr in self.fighter.itemModifiedAttributes or self.fighter.charge is not None

    @property
    def grouped(self):
        # is the ability applied per fighter (webs, returns False), or as a group (MWD, returned True)
        return self.__effect.getattr('grouped')

    @property
    def hasCharges(self):
        return self.__effect.getattr('hasCharges')

    @property
    def reloadTime(self):
        return self.getReloadTime()

    def getReloadTime(self, spentShots=None):
        if spentShots is not None:
            spentShots = max(self.numShots, spentShots)
        else:
            spentShots = self.numShots
        rearm_time = (self.REARM_TIME_MAPPING[self.fighter.getModifiedItemAttr("fighterSquadronRole")] or 0 if self.hasCharges else 0)
        return self.fighter.getModifiedItemAttr("fighterRefuelingTime") + rearm_time * spentShots

    @property
    def numShots(self):
        return self.NUM_SHOTS_MAPPING[self.fighter.getModifiedItemAttr("fighterSquadronRole")] or 0 if self.hasCharges else 0

    @property
    def cycleTime(self):
        speed = self.fighter.getModifiedItemAttr("{}Duration".format(self.attrPrefix))
        return speed

    def getVolley(self, targetProfile=None):
        if not self.dealsDamage or not self.active:
            return DmgTypes(0, 0, 0, 0)
        if self.attrPrefix == "fighterAbilityLaunchBomb":
            em = self.fighter.getModifiedChargeAttr("emDamage", 0)
            therm = self.fighter.getModifiedChargeAttr("thermalDamage", 0)
            kin = self.fighter.getModifiedChargeAttr("kineticDamage", 0)
            exp = self.fighter.getModifiedChargeAttr("explosiveDamage", 0)
        else:
            em = self.fighter.getModifiedItemAttr("{}DamageEM".format(self.attrPrefix), 0)
            therm = self.fighter.getModifiedItemAttr("{}DamageTherm".format(self.attrPrefix), 0)
            kin = self.fighter.getModifiedItemAttr("{}DamageKin".format(self.attrPrefix), 0)
            exp = self.fighter.getModifiedItemAttr("{}DamageExp".format(self.attrPrefix), 0)
        dmgMult = self.fighter.amount * self.fighter.getModifiedItemAttr("{}DamageMultiplier".format(self.attrPrefix), 1)
        volley = DmgTypes(
            em=em * dmgMult * (1 - getattr(targetProfile, "emAmount", 0)),
            thermal=therm * dmgMult * (1 - getattr(targetProfile, "thermalAmount", 0)),
            kinetic=kin * dmgMult * (1 - getattr(targetProfile, "kineticAmount", 0)),
            explosive=exp * dmgMult * (1 - getattr(targetProfile, "explosiveAmount", 0)))
        return volley

    def getDps(self, targetProfile=None, cycleTimeOverride=None):
        volley = self.getVolley(targetProfile=targetProfile)
        if not volley:
            return DmgTypes(0, 0, 0, 0)
        cycleTime = cycleTimeOverride if cycleTimeOverride is not None else self.cycleTime
        dpsFactor = 1 / (cycleTime / 1000)
        dps = DmgTypes(
            em=volley.em * dpsFactor,
            thermal=volley.thermal * dpsFactor,
            kinetic=volley.kinetic * dpsFactor,
            explosive=volley.explosive * dpsFactor)
        return dps

    def clear(self):
        pass
