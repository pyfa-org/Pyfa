#===============================================================================
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
#===============================================================================

from eos.graph import Graph, Data
from eos.types import Hardpoint, State
from math import log, sin, radians, exp

class FitDpsGraph(Graph):
    defaults = {"angle": 0,
                "distance": 0,
                "signatureRadius": None,
                "velocity": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcDps, data if data is not None else self.defaults)
        self.fit = fit

    def calcDps(self, data):
        ew = {'signatureRadius':[],'velocity':[]}
        fit = self.fit
        total = 0
        distance = data["distance"] * 1000
        abssort = lambda val: -abs(val - 1)

        for mod in fit.modules:
            if not mod.isEmpty and mod.state >= State.ACTIVE:
                if "ewTargetPaint" in mod.item.effects:
                    ew['signatureRadius'].append(1+(mod.getModifiedItemAttr("signatureRadiusBonus") / 100))
                if "decreaseTargetSpeed" in mod.item.effects:
                    ew['velocity'].append(1+(mod.getModifiedItemAttr("speedFactor") / 100))

        ew['signatureRadius'].sort(key=abssort)
        ew['velocity'].sort(key=abssort)

        for attr, values in ew.iteritems():
            val = data[attr]
            try:
                for i in xrange(len(values)):
                    bonus = values[i]
                    val *= 1 + (bonus - 1) * exp(- i ** 2 / 7.1289)
                data[attr] = val
            except:
                pass

        for mod in fit.modules:
            dps, _ =  mod.damageStats(fit.targetResists)
            if mod.hardpoint == Hardpoint.TURRET:
                if mod.state >= State.ACTIVE:
                    total += dps * self.calculateTurretMultiplier(mod, data)

            elif mod.hardpoint == Hardpoint.MISSILE:
                if mod.state >= State.ACTIVE and mod.maxRange >= distance:
                    total += dps * self.calculateMissileMultiplier(mod, data)

        if distance <= fit.extraAttributes["droneControlRange"]:
            for drone in fit.drones:
                multiplier = 1 if drone.getModifiedItemAttr("maxVelocity") > 0 else self.calculateTurretMultiplier(drone, data)
                dps, _ =  drone.damageStats(fit.targetResists)
                total += dps * multiplier
        return total

    def calculateMissileMultiplier(self, mod, data):
        targetSigRad = data["signatureRadius"]
        targetVelocity = data["velocity"]
        explosionRadius = mod.getModifiedChargeAttr("aoeCloudSize")
        targetSigRad = explosionRadius if targetSigRad is None else targetSigRad
        explosionVelocity = mod.getModifiedChargeAttr("aoeVelocity")
        damageReductionFactor = mod.getModifiedChargeAttr("aoeDamageReductionFactor")
        damageReductionSensitivity = mod.getModifiedChargeAttr("aoeDamageReductionSensitivity")

        sigRadiusFactor = targetSigRad / explosionRadius
        if targetVelocity:
            velocityFactor = (explosionVelocity / explosionRadius * targetSigRad / targetVelocity) ** (log(damageReductionFactor) / log(damageReductionSensitivity))
        else:
            velocityFactor = 1

        return min(sigRadiusFactor, velocityFactor, 1)

    def calculateTurretMultiplier(self, mod, data):
        #Source for most of turret calculation info: http://wiki.eveonline.com/en/wiki/Falloff
        chanceToHit = self.calculateTurretChanceToHit(mod, data)
        if chanceToHit > 0.01:
            #AvgDPS = Base Damage * [ ( ChanceToHit^2 + ChanceToHit + 0.0499 ) / 2 ]
            multiplier = (chanceToHit ** 2 + chanceToHit + 0.0499) / 2
        else:
            #All hits are wreckings
            multiplier = chanceToHit * 3
        dmgScaling = mod.getModifiedItemAttr("turretDamageScalingRadius")
        if dmgScaling:
            targetSigRad = data["signatureRadius"]
            multiplier = min(1, (float(targetSigRad) / dmgScaling) ** 2)
        return multiplier

    def calculateTurretChanceToHit(self, mod, data):
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
