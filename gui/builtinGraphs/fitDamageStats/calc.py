# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import math
from functools import lru_cache

from service.const import GraphDpsDroneMode
from service.settings import GraphSettings


def getTurretMult(mod, fit, tgt, atkSpeed, atkAngle, distance, tgtSpeed, tgtAngle, tgtSigRadius):
    cth = _calcTurretChanceToHit(
        atkSpeed=atkSpeed,
        atkAngle=atkAngle,
        atkRadius=fit.ship.getModifiedItemAttr('radius'),
        atkOptimalRange=mod.maxRange,
        atkFalloffRange=mod.falloff,
        atkTracking=mod.getModifiedItemAttr('trackingSpeed'),
        atkOptimalSigRadius=mod.getModifiedItemAttr('optimalSigRadius'),
        distance=distance,
        tgtSpeed=tgtSpeed,
        tgtAngle=tgtAngle,
        tgtRadius=tgt.ship.getModifiedItemAttr('radius'),
        tgtSigRadius=tgtSigRadius)
    mult = _calcTurretMult(cth)
    return mult


def getLauncherMult(mod, fit, distance, tgtSpeed, tgtSigRadius):
    modRange = mod.maxRange
    if modRange is None:
        return 0
    if distance + fit.ship.getModifiedItemAttr('radius') > modRange:
        return 0
    mult = _calcMissileFactor(
        atkEr=mod.getModifiedChargeAttr('aoeCloudSize'),
        atkEv=mod.getModifiedChargeAttr('aoeVelocity'),
        atkDrf=mod.getModifiedChargeAttr('aoeDamageReductionFactor'),
        tgtSpeed=tgtSpeed,
        tgtSigRadius=tgtSigRadius)
    return mult


def getSmartbombMult(mod, distance):
    modRange = mod.maxRange
    if modRange is None:
        return 0
    if distance > modRange:
        return 0
    return 1


def getBombMult(mod, fit, tgt, distance, tgtSigRadius):
    modRange = mod.maxRange
    if modRange is None:
        return 0
    blastRadius = mod.getModifiedChargeAttr('explosionRange')
    atkRadius = fit.ship.getModifiedItemAttr('radius')
    tgtRadius = tgt.ship.getModifiedItemAttr('radius')
    # Bomb starts in the center of the ship
    # Also here we assume that it affects target as long as blast
    # touches its surface, not center - I did not check this
    if distance < max(0, modRange - atkRadius - tgtRadius - blastRadius):
        return 0
    if distance > max(0, modRange - atkRadius + tgtRadius + blastRadius):
        return 0
    return _calcBombFactor(
        atkEr=mod.getModifiedChargeAttr('aoeCloudSize'),
        tgtSigRadius=tgtSigRadius)


def getGuidedBombMult(mod, fit, distance, tgtSigRadius):
    modRange = mod.maxRange
    if modRange is None:
        return 0
    if distance > modRange - fit.ship.getModifiedItemAttr('radius'):
        return 0
    eR = mod.getModifiedChargeAttr('aoeCloudSize')
    if eR == 0:
        return 1
    else:
        return min(1, tgtSigRadius / eR)


def getDroneMult(drone, fit, tgt, atkSpeed, atkAngle, distance, tgtSpeed, tgtAngle, tgtSigRadius):
    if distance > fit.extraAttributes['droneControlRange']:
        return 0
    droneSpeed = drone.getModifiedItemAttr('maxVelocity')
    # Hard to simulate drone behavior, so assume chance to hit is 1 for mobile drones
    # which catch up with target
    droneOpt = GraphSettings.getInstance().get('mobileDroneMode')
    if (
        droneSpeed > 1 and (
            (droneOpt == GraphDpsDroneMode.auto and droneSpeed >= tgtSpeed) or
            droneOpt == GraphDpsDroneMode.followTarget)
    ):
        cth = 1
    # Otherwise put the drone into center of the ship, move it at its max speed or ship's speed
    # (whichever is lower) towards direction of attacking ship and see how well it projects
    else:
        droneRadius = drone.getModifiedItemAttr('radius')
        cth = _calcTurretChanceToHit(
            atkSpeed=min(atkSpeed, droneSpeed),
            atkAngle=atkAngle,
            atkRadius=droneRadius,
            atkOptimalRange=drone.maxRange,
            atkFalloffRange=drone.falloff,
            atkTracking=drone.getModifiedItemAttr('trackingSpeed'),
            atkOptimalSigRadius=drone.getModifiedItemAttr('optimalSigRadius'),
            # As distance is ship surface to ship surface, we adjust it according
            # to attacker fit's radiuses to have drone surface to ship surface distance
            distance=distance + fit.ship.getModifiedItemAttr('radius') - droneRadius,
            tgtSpeed=tgtSpeed,
            tgtAngle=tgtAngle,
            tgtRadius=tgt.ship.getModifiedItemAttr('radius'),
            tgtSigRadius=tgtSigRadius)
    mult = _calcTurretMult(cth)
    return mult


def getFighterAbilityMult(fighter, ability, fit, distance, tgtSpeed, tgtSigRadius):
    fighterSpeed = fighter.getModifiedItemAttr('maxVelocity')
    attrPrefix = ability.attrPrefix
    # It's bomb attack
    if attrPrefix == 'fighterAbilityLaunchBomb':
        # Just assume we can land bomb anywhere
        return _calcBombFactor(
            atkEr=fighter.getModifiedChargeAttr('aoeCloudSize'),
            tgtSigRadius=tgtSigRadius)
    droneOpt = GraphSettings.getInstance().get('mobileDroneMode')
    # It's regular missile-based attack
    if (droneOpt == GraphDpsDroneMode.auto and fighterSpeed >= tgtSpeed) or droneOpt == GraphDpsDroneMode.followTarget:
        rangeFactor = 1
    # Same as with drones, if fighters are slower - put them to center of
    # the ship and see how they apply
    else:
        rangeFactor = _calcRangeFactor(
            atkOptimalRange=fighter.getModifiedItemAttr('{}RangeOptimal'.format(attrPrefix)),
            atkFalloffRange=fighter.getModifiedItemAttr('{}RangeFalloff'.format(attrPrefix)),
            distance=distance + fit.ship.getModifiedItemAttr('radius') - fighter.getModifiedItemAttr('radius'))
    drf = fighter.getModifiedItemAttr('{}ReductionFactor'.format(attrPrefix), None)
    if drf is None:
        drf = fighter.getModifiedItemAttr('{}DamageReductionFactor'.format(attrPrefix))
    drs = fighter.getModifiedItemAttr('{}ReductionSensitivity'.format(attrPrefix), None)
    if drs is None:
        drs = fighter.getModifiedItemAttr('{}DamageReductionSensitivity'.format(attrPrefix))
    missileFactor = _calcMissileFactor(
        atkEr=fighter.getModifiedItemAttr('{}ExplosionRadius'.format(attrPrefix)),
        atkEv=fighter.getModifiedItemAttr('{}ExplosionVelocity'.format(attrPrefix)),
        atkDrf=_calcAggregatedDrf(reductionFactor=drf, reductionSensitivity=drs),
        tgtSpeed=tgtSpeed,
        tgtSigRadius=tgtSigRadius)
    mult = rangeFactor * missileFactor
    return mult


def applyWebs(tgt, currentUnwebbedSpeed, webMods, distance):
    unwebbedSpeed = tgt.ship.getModifiedItemAttr('maxVelocity')
    try:
        speedRatio = currentUnwebbedSpeed / unwebbedSpeed
    except ZeroDivisionError:
        currentWebbedSpeed = 0
    else:
        appliedMultipliers = {}
        for boost, optimal, falloff, stackingChain in webMods:
            appliedBoost = boost * _calcRangeFactor(atkOptimalRange=optimal, atkFalloffRange=falloff, distance=distance)
            if appliedBoost:
                appliedMultipliers.setdefault(stackingChain, []).append(1 + appliedBoost / 100)
        webbedSpeed = tgt.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=appliedMultipliers)
        currentWebbedSpeed = webbedSpeed * speedRatio
    return currentWebbedSpeed


def applyTps(tgt, tpMods, distance):
    untpedSig = tgt.ship.getModifiedItemAttr('signatureRadius')
    appliedMultipliers = {}
    for boost, optimal, falloff, stackingChain in tpMods:
        appliedBoost = boost * _calcRangeFactor(atkOptimalRange=optimal, atkFalloffRange=falloff, distance=distance)
        if appliedBoost:
            appliedMultipliers.setdefault(stackingChain, []).append(1 + appliedBoost / 100)
    tpedSig = tgt.ship.getModifiedItemAttrWithExtraMods('signatureRadius', extraMultipliers=appliedMultipliers)
    mult = tpedSig / untpedSig
    return mult


# Turret-specific
@lru_cache(maxsize=50)
def _calcTurretMult(chanceToHit):
    """Calculate damage multiplier for turret-based weapons."""
    # https://wiki.eveuniversity.org/Turret_mechanics#Damage
    wreckingChance = min(chanceToHit, 0.01)
    wreckingPart = wreckingChance * 3
    normalChance = chanceToHit - wreckingChance
    if normalChance > 0:
        avgDamageMult = (0.01 + chanceToHit) / 2 + 0.49
        normalPart = normalChance * avgDamageMult
    else:
        normalPart = 0
    totalMult = normalPart + wreckingPart
    return totalMult


@lru_cache(maxsize=1000)
def _calcTurretChanceToHit(
    atkSpeed, atkAngle, atkRadius, atkOptimalRange, atkFalloffRange, atkTracking, atkOptimalSigRadius,
    distance, tgtSpeed, tgtAngle, tgtRadius, tgtSigRadius
):
    """Calculate chance to hit for turret-based weapons."""
    # https://wiki.eveuniversity.org/Turret_mechanics#Hit_Math
    angularSpeed = _calcAngularSpeed(atkSpeed, atkAngle, atkRadius, distance, tgtSpeed, tgtAngle, tgtRadius)
    rangeFactor = _calcRangeFactor(atkOptimalRange, atkFalloffRange, distance)
    trackingFactor = _calcTrackingFactor(atkTracking, atkOptimalSigRadius, angularSpeed, tgtSigRadius)
    cth = rangeFactor * trackingFactor
    return cth


def _calcAngularSpeed(atkSpeed, atkAngle, atkRadius, distance, tgtSpeed, tgtAngle, tgtRadius):
    """Calculate angular speed based on mobility parameters of two ships."""
    atkAngle = atkAngle * math.pi / 180
    tgtAngle = tgtAngle * math.pi / 180
    ctcDistance = atkRadius + distance + tgtRadius
    # Target is to the right of the attacker, so transversal is projection onto Y axis
    transSpeed = abs(atkSpeed * math.sin(atkAngle) - tgtSpeed * math.sin(tgtAngle))
    if ctcDistance == 0:
        angularSpeed = 0 if transSpeed == 0 else math.inf
    else:
        angularSpeed = transSpeed / ctcDistance
    return angularSpeed


def _calcTrackingFactor(atkTracking, atkOptimalSigRadius, angularSpeed, tgtSigRadius):
    """Calculate tracking chance to hit component."""
    return 0.5 ** (((angularSpeed * atkOptimalSigRadius) / (atkTracking * tgtSigRadius)) ** 2)


# Missile-specific
@lru_cache(maxsize=200)
def _calcMissileFactor(atkEr, atkEv, atkDrf, tgtSpeed, tgtSigRadius):
    """Missile application."""
    factors = [1]
    # "Slow" part
    if atkEr > 0:
        factors.append(tgtSigRadius / atkEr)
    # "Fast" part
    if tgtSpeed > 0:
        factors.append(((atkEv * tgtSigRadius) / (atkEr * tgtSpeed)) ** atkDrf)
    totalMult = min(factors)
    return totalMult


def _calcAggregatedDrf(reductionFactor, reductionSensitivity):
    """
    Sometimes DRF is specified as 2 separate numbers,
    here we combine them into generic form.
    """
    return math.log(reductionFactor) / math.log(reductionSensitivity)


# Generic
def _calcRangeFactor(atkOptimalRange, atkFalloffRange, distance):
    """Range strength/chance factor, applicable to guns, ewar, RRs, etc."""
    if atkFalloffRange > 0:
        factor = 0.5 ** ((max(0, distance - atkOptimalRange) / atkFalloffRange) ** 2)
    elif distance <= atkOptimalRange:
        factor = 1
    else:
        factor = 0
    return factor


def _calcBombFactor(atkEr, tgtSigRadius):
    if atkEr == 0:
        return 1
    else:
        return min(1, tgtSigRadius / atkEr)
