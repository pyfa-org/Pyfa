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


from math import exp, log, radians, sin, inf

from logbook import Logger

import eos.config
from eos.const import FittingHardpoint, FittingModuleState
from eos.graph import SmoothGraph
from eos.utils.spoolSupport import SpoolType, SpoolOptions


pyfalog = Logger(__name__)


class FitDpsVsRangeGraph(SmoothGraph):

    def getYForX(self, fit, extraData, distance):
        tgtSpeed = extraData['speed']
        tgtSigRad = extraData['signatureRadius'] if extraData['signatureRadius'] is not None else inf
        angle = extraData['angle']
        tgtSigRadMods = []
        tgtSpeedMods = []
        total = 0
        distance = distance * 1000

        for mod in fit.modules:
            if not mod.isEmpty and mod.state >= FittingModuleState.ACTIVE:
                if "remoteTargetPaintFalloff" in mod.item.effects or "structureModuleEffectTargetPainter" in mod.item.effects:
                    tgtSigRadMods.append(
                        1 + (mod.getModifiedItemAttr("signatureRadiusBonus") / 100)
                        * self.calculateModuleMultiplier(mod, distance))
                if "remoteWebifierFalloff" in mod.item.effects or "structureModuleEffectStasisWebifier" in mod.item.effects:
                    if distance <= mod.getModifiedItemAttr("maxRange"):
                        tgtSpeedMods.append(1 + (mod.getModifiedItemAttr("speedFactor") / 100))
                    elif mod.getModifiedItemAttr("falloffEffectiveness") > 0:
                        # I am affected by falloff
                        tgtSpeedMods.append(
                            1 + (mod.getModifiedItemAttr("speedFactor") / 100) *
                            self.calculateModuleMultiplier(mod, distance))

        tgtSpeed = self.penalizeModChain(tgtSpeed, tgtSpeedMods)
        tgtSigRad = self.penalizeModChain(tgtSigRad, tgtSigRadMods)
        attRad = fit.ship.getModifiedItemAttr('radius', 0)
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']

        for mod in fit.modules:
            dps = mod.getDps(targetResists=fit.targetResists, spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False)).total
            if mod.hardpoint == FittingHardpoint.TURRET:
                if mod.state >= FittingModuleState.ACTIVE:
                    total += dps * self.calculateTurretMultiplier(fit, mod, distance, angle, tgtSpeed, tgtSigRad)

            elif mod.hardpoint == FittingHardpoint.MISSILE:
                if mod.state >= FittingModuleState.ACTIVE and mod.maxRange is not None and (mod.maxRange - attRad) >= distance:
                    total += dps * self.calculateMissileMultiplier(mod, tgtSpeed, tgtSigRad)

        if distance <= fit.extraAttributes['droneControlRange']:
            for drone in fit.drones:
                multiplier = 1 if drone.getModifiedItemAttr('maxVelocity') > 1 else self.calculateTurretMultiplier(
                    fit, drone, distance, angle, tgtSpeed, tgtSigRad)
                dps = drone.getDps(targetResists=fit.targetResists).total
                total += dps * multiplier

        # this is janky as fuck
        for fighter in fit.fighters:
            if not fighter.active:
                continue
            fighterDpsMap = fighter.getDpsPerEffect(targetResists=fit.targetResists)
            for ability in fighter.abilities:
                if ability.dealsDamage and ability.active:
                    if ability.effectID not in fighterDpsMap:
                        continue
                    multiplier = self.calculateFighterMissileMultiplier(tgtSpeed, tgtSigRad, ability)
                    dps = fighterDpsMap[ability.effectID].total
                    total += dps * multiplier

        return total

    @staticmethod
    def calculateMissileMultiplier(mod, tgtSpeed, tgtSigRad):
        explosionRadius = mod.getModifiedChargeAttr('aoeCloudSize')
        explosionVelocity = mod.getModifiedChargeAttr('aoeVelocity')
        damageReductionFactor = mod.getModifiedChargeAttr('aoeDamageReductionFactor')

        sigRadiusFactor = tgtSigRad / explosionRadius
        if tgtSpeed:
            velocityFactor = (explosionVelocity / explosionRadius * tgtSigRad / tgtSpeed) ** damageReductionFactor
        else:
            velocityFactor = 1

        return min(sigRadiusFactor, velocityFactor, 1)

    @classmethod
    def calculateTurretMultiplier(cls, fit, mod, distance, angle, tgtSpeed, tgtSigRad):
        # Source for most of turret calculation info: http://wiki.eveonline.com/en/wiki/Falloff
        chanceToHit = cls.calculateTurretChanceToHit(fit, mod, distance, angle, tgtSpeed, tgtSigRad)
        if chanceToHit > 0.01:
            # AvgDPS = Base Damage * [ ( ChanceToHit^2 + ChanceToHit + 0.0499 ) / 2 ]
            multiplier = (chanceToHit ** 2 + chanceToHit + 0.0499) / 2
        else:
            # All hits are wreckings
            multiplier = chanceToHit * 3
        dmgScaling = mod.getModifiedItemAttr('turretDamageScalingRadius')
        if dmgScaling:
            multiplier = min(1, (float(tgtSigRad) / dmgScaling) ** 2)
        return multiplier

    @staticmethod
    def calculateFighterMissileMultiplier(tgtSpeed, tgtSigRad, ability):
        prefix = ability.attrPrefix

        explosionRadius = ability.fighter.getModifiedItemAttr('{}ExplosionRadius'.format(prefix))
        explosionVelocity = ability.fighter.getModifiedItemAttr('{}ExplosionVelocity'.format(prefix))
        damageReductionFactor = ability.fighter.getModifiedItemAttr('{}ReductionFactor'.format(prefix), None)

        # the following conditionals are because CCP can't keep a decent naming convention, as if fighter implementation
        # wasn't already fucked.
        if damageReductionFactor is None:
            damageReductionFactor = ability.fighter.getModifiedItemAttr('{}DamageReductionFactor'.format(prefix))

        damageReductionSensitivity = ability.fighter.getModifiedItemAttr('{}ReductionSensitivity'.format(prefix), None)
        if damageReductionSensitivity is None:
            damageReductionSensitivity = ability.fighter.getModifiedItemAttr('{}DamageReductionSensitivity'.format(prefix))

        sigRadiusFactor = tgtSigRad / explosionRadius

        if tgtSpeed:
            velocityFactor = (explosionVelocity / explosionRadius * tgtSigRad / tgtSpeed) ** (
                log(damageReductionFactor) / log(damageReductionSensitivity))
        else:
            velocityFactor = 1

        return min(sigRadiusFactor, velocityFactor, 1)

    @staticmethod
    def calculateTurretChanceToHit(fit, mod, distance, angle, tgtSpeed, tgtSigRad):
        tracking = mod.getModifiedItemAttr('trackingSpeed')
        turretOptimal = mod.maxRange
        turretFalloff = mod.falloff
        turretSigRes = mod.getModifiedItemAttr('optimalSigRadius')
        transversal = sin(radians(angle)) * tgtSpeed

        # Angular velocity is calculated using range from ship center to target center.
        # We do not know target radius but we know attacker radius
        angDistance = distance + fit.ship.getModifiedItemAttr('radius', 0)
        if angDistance == 0 and transversal == 0:
            angularVelocity = 0
        elif angDistance == 0 and transversal != 0:
            angularVelocity = inf
        else:
            angularVelocity = transversal / angDistance
        trackingEq = (((angularVelocity / tracking) *
                       (turretSigRes / tgtSigRad)) ** 2)
        rangeEq = ((max(0, distance - turretOptimal)) / turretFalloff) ** 2

        return 0.5 ** (trackingEq + rangeEq)

    @staticmethod
    def calculateModuleMultiplier(mod, distance):
        # Simplified formula, we make some assumptions about the module
        # This is basically the calculateTurretChanceToHit without tracking values
        turretOptimal = mod.maxRange
        turretFalloff = mod.falloff
        rangeEq = ((max(0, distance - turretOptimal)) / turretFalloff) ** 2

        return 0.5 ** rangeEq

    @staticmethod
    def penalizeModChain(value, mods):
        mods.sort(key=lambda v: -abs(v - 1))
        try:
            for i in range(len(mods)):
                bonus = mods[i]
                value *= 1 + (bonus - 1) * exp(- i ** 2 / 7.1289)
            return value
        except Exception as e:
            pyfalog.critical('Caught exception when penalizing modifier chain.')
            pyfalog.critical(e)
            return value
