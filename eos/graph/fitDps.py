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

from math import log, sin, radians, exp

from eos.graph import Graph
from eos.saveddata.module import State, Hardpoint
from logbook import Logger

pyfalog = Logger(__name__)


class FitDpsGraph(Graph):
    defaults = {
        "angle"          : 0,
        "distance"       : 0,
        "signatureRadius": None,
        "velocity"       : 0
    }

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcDps, data if data is not None else self.defaults)
        self.fit = fit

    def calcDps(self, data):
        ew = {'signatureRadius': [], 'velocity': []}
        fit = self.fit
        total = 0
        distance = data["distance"] * 1000
        abssort = lambda _val: -abs(_val - 1)

        for mod in fit.modules:
            if not mod.isEmpty and mod.state >= State.ACTIVE:
                if "remoteTargetPaintFalloff" in mod.item.effects or "structureModuleEffectTargetPainter" in mod.item.effects:
                    ew['signatureRadius'].append(
                            1 + (mod.getModifiedItemAttr("signatureRadiusBonus") / 100) * self.calculateModuleMultiplier(
                                    mod, data))
                if "remoteWebifierFalloff" in mod.item.effects or "structureModuleEffectStasisWebifier" in mod.item.effects:
                    if distance <= mod.getModifiedItemAttr("maxRange"):
                        ew['velocity'].append(1 + (mod.getModifiedItemAttr("speedFactor") / 100))
                    elif mod.getModifiedItemAttr("falloffEffectiveness") > 0:
                        # I am affected by falloff
                        ew['velocity'].append(
                                1 + (mod.getModifiedItemAttr("speedFactor") / 100) * self.calculateModuleMultiplier(mod,
                                                                                                                    data))

        ew['signatureRadius'].sort(key=abssort)
        ew['velocity'].sort(key=abssort)

        for attr, values in ew.iteritems():
            val = data[attr]
            try:
                for i in xrange(len(values)):
                    bonus = values[i]
                    val *= 1 + (bonus - 1) * exp(- i ** 2 / 7.1289)
                data[attr] = val
            except Exception as e:
                pyfalog.critical("Caught exception in calcDPS.")
                pyfalog.critical(e)

        for mod in fit.modules:
            dps, _ = mod.damageStats(fit.targetResists)
            if mod.hardpoint == Hardpoint.TURRET:
                if mod.state >= State.ACTIVE:
                    total += dps * self.calculateTurretMultiplier(mod, data)

            elif mod.hardpoint == Hardpoint.MISSILE:
                if mod.state >= State.ACTIVE and mod.maxRange >= distance:
                    total += dps * self.calculateMissileMultiplier(mod, data)

        if distance <= fit.extraAttributes["droneControlRange"]:
            for drone in fit.drones:
                multiplier = 1 if drone.getModifiedItemAttr("maxVelocity") > 1 else self.calculateTurretMultiplier(
                        drone, data)
                dps, _ = drone.damageStats(fit.targetResists)
                total += dps * multiplier

        # this is janky as fuck
        for fighter in fit.fighters:
            for ability in fighter.abilities:
                if ability.dealsDamage and ability.active:
                    multiplier = self.calculateFighterMissileMultiplier(ability, data)
                    dps, _ = ability.damageStats(fit.targetResists)
                    total += dps * multiplier

        return total

    @staticmethod
    def calculateMissileMultiplier(mod, data):
        targetSigRad = data["signatureRadius"]
        targetVelocity = data["velocity"]
        explosionRadius = mod.getModifiedChargeAttr("aoeCloudSize")
        targetSigRad = explosionRadius if targetSigRad is None else targetSigRad
        explosionVelocity = mod.getModifiedChargeAttr("aoeVelocity")
        damageReductionFactor = mod.getModifiedChargeAttr("aoeDamageReductionFactor")

        sigRadiusFactor = targetSigRad / explosionRadius
        if targetVelocity:
            velocityFactor = (explosionVelocity / explosionRadius * targetSigRad / targetVelocity) ** damageReductionFactor
        else:
            velocityFactor = 1

        return min(sigRadiusFactor, velocityFactor, 1)

    def calculateTurretMultiplier(self, mod, data):
        # Source for most of turret calculation info: http://wiki.eveonline.com/en/wiki/Falloff
        chanceToHit = self.calculateTurretChanceToHit(mod, data)
        if chanceToHit > 0.01:
            # AvgDPS = Base Damage * [ ( ChanceToHit^2 + ChanceToHit + 0.0499 ) / 2 ]
            multiplier = (chanceToHit ** 2 + chanceToHit + 0.0499) / 2
        else:
            # All hits are wreckings
            multiplier = chanceToHit * 3
        dmgScaling = mod.getModifiedItemAttr("turretDamageScalingRadius")
        if dmgScaling:
            targetSigRad = data["signatureRadius"]
            multiplier = min(1, (float(targetSigRad) / dmgScaling) ** 2)
        return multiplier

    @staticmethod
    def calculateFighterMissileMultiplier(ability, data):
        prefix = ability.attrPrefix

        targetSigRad = data["signatureRadius"]
        targetVelocity = data["velocity"]
        explosionRadius = ability.fighter.getModifiedItemAttr("{}ExplosionRadius".format(prefix))
        explosionVelocity = ability.fighter.getModifiedItemAttr("{}ExplosionVelocity".format(prefix))
        damageReductionFactor = ability.fighter.getModifiedItemAttr("{}ReductionFactor".format(prefix))

        # the following conditionals are because CCP can't keep a decent naming convention, as if fighter implementation
        # wasn't already fucked.
        if damageReductionFactor is None:
            damageReductionFactor = ability.fighter.getModifiedItemAttr("{}DamageReductionFactor".format(prefix))

        damageReductionSensitivity = ability.fighter.getModifiedItemAttr("{}ReductionSensitivity".format(prefix))
        if damageReductionSensitivity is None:
            damageReductionSensitivity = ability.fighter.getModifiedItemAttr(
                    "{}DamageReductionSensitivity".format(prefix))

        targetSigRad = explosionRadius if targetSigRad is None else targetSigRad
        sigRadiusFactor = targetSigRad / explosionRadius

        if targetVelocity:
            velocityFactor = (explosionVelocity / explosionRadius * targetSigRad / targetVelocity) ** (
                log(damageReductionFactor) / log(damageReductionSensitivity))
        else:
            velocityFactor = 1

        return min(sigRadiusFactor, velocityFactor, 1)

    @staticmethod
    def calculateTurretChanceToHit(mod, data):
        distance = data["distance"] * 1000
        tracking = mod.getModifiedItemAttr("trackingSpeed")
        turretOptimal = mod.maxRange
        turretFalloff = mod.falloff
        turretSigRes = mod.getModifiedItemAttr("optimalSigRadius")
        targetSigRad = data["signatureRadius"]
        targetSigRad = turretSigRes if targetSigRad is None else targetSigRad
        transversal = sin(radians(data["angle"])) * data["velocity"]
        trackingEq = (((transversal / (distance * tracking)) *
                       (turretSigRes / targetSigRad)) ** 2)
        rangeEq = ((max(0, distance - turretOptimal)) / turretFalloff) ** 2

        return 0.5 ** (trackingEq + rangeEq)

    @staticmethod
    def calculateModuleMultiplier(mod, data):
        # Simplified formula, we make some assumptions about the module
        # This is basically the calculateTurretChanceToHit without tracking values
        distance = data["distance"] * 1000
        turretOptimal = mod.maxRange
        turretFalloff = mod.falloff
        rangeEq = ((max(0, distance - turretOptimal)) / turretFalloff) ** 2

        return 0.5 ** rangeEq
