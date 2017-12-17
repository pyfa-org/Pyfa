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
from math import log

pyfalog = Logger(__name__)


class FighterAbility(object):
    DAMAGE_TYPES = ("em", "kinetic", "explosive", "thermal")
    DAMAGE_TYPES2 = ("EM", "Kin", "Exp", "Therm")

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
            self.__effect = next((x for x in self.fighter.item.effects.itervalues() if x.ID == self.effectID), None)
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
        return self.__effect.getattr('displayName') or self.__effect.handlerName

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
        rearm_time = (self.REARM_TIME_MAPPING[self.fighter.getModifiedItemAttr("fighterSquadronRole")] or 0 if self.hasCharges else 0)
        return self.fighter.getModifiedItemAttr("fighterRefuelingTime") + rearm_time * self.numShots

    @property
    def numShots(self):
        return self.NUM_SHOTS_MAPPING[self.fighter.getModifiedItemAttr("fighterSquadronRole")] or 0 if self.hasCharges else 0

    @property
    def cycleTime(self):
        speed = self.fighter.getModifiedItemAttr("{}Duration".format(self.attrPrefix))

        # Factor in reload
        '''
        reload = self.reloadTime

        if self.fighter.owner.factorReload:
            numShots = self.numShots
            # Speed here already takes into consideration reactivation time
            speed = (speed * numShots + reload) / numShots if numShots > 0 else speed
        '''

        return speed

    def calculateAbilityMultiplier(self, signatureRadius, speed):
        explosionRadius = self.fighter.getModifiedItemAttr("{}ExplosionRadius".format(self.attrPrefix))
        explosionVelocity = self.fighter.getModifiedItemAttr("{}ExplosionVelocity".format(self.attrPrefix))
        damageReductionFactor = self.fighter.getModifiedItemAttr("{}ReductionFactor".format(self.attrPrefix))
        damageReductionSensitivity = self.fighter.getModifiedItemAttr("{}ReductionSensitivity".format(self.attrPrefix))

        # the following conditionals are because CCP can't keep a decent naming convention, as if fighter implementation
        # wasn't already fucked.
        if damageReductionFactor is None:
            damageReductionFactor = self.fighter.getModifiedItemAttr("{}DamageReductionFactor".format(self.attrPrefix))
        if damageReductionSensitivity is None:
            damageReductionSensitivity = self.fighter.getModifiedItemAttr("{}DamageReductionSensitivity".format(self.attrPrefix))

        signatureRadius = signatureRadius or explosionRadius
        sigRadiusFactor = signatureRadius / explosionRadius

        velocityFactor = 1
        if speed:
            velocityFactor = (explosionVelocity / explosionRadius * signatureRadius / speed) ** (
                log(damageReductionFactor) / log(damageReductionSensitivity))

        return min(sigRadiusFactor, velocityFactor, 1)

    def damageStats(self, emRes=0, thRes=0, kiRes=0, exRes=0, distance=0, signatureRadius=0, speed=0, transversal=0):
        if (not self.active) or (not self.dealsDamage) or (self.fighter.amountActive < 1):
            return 0, 0

        dps = 0
        if self.attrPrefix == "fighterAbilityLaunchBomb":
            # bomb calcs
            volley = sum(((self.fighter.getModifiedChargeAttr("{}Damage".format(dtype)) or 0) * (1 - res)) for dtype,res in zip(self.DAMAGE_TYPES,(emRes,thRes,kiRes,exRes)))
        else:
            volley = sum(((self.fighter.getModifiedItemAttr("{}Damage{}".format(self.attrPrefix, dtype)) or 0) * (1 - res)) for dtype,res in zip(self.DAMAGE_TYPES2,(emRes,thRes,kiRes,exRes)))

        if volley:
            volley *= self.fighter.amountActive
            volley *= self.fighter.getModifiedItemAttr("{}DamageMultiplier".format(self.attrPrefix)) or 1
            if signatureRadius or speed:
                volley *= self.calculateAbilityMultiplier(signatureRadius, speed)
            volley = volley or 0
            dps = volley / (self.cycleTime / 1000.0)

        return dps, volley

    def clear(self):
        pass
