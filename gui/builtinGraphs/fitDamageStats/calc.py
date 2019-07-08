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


def getWebbedSpeed(fit, tgt, currentUnwebbedSpeed, webMods, webDrones, webFighters, distance):
    if tgt.ship.getModifiedItemAttr('disallowOffensiveModifiers'):
        return currentUnwebbedSpeed
    maxUnwebbedSpeed = tgt.ship.getModifiedItemAttr('maxVelocity')
    try:
        speedRatio = currentUnwebbedSpeed / maxUnwebbedSpeed
    except ZeroDivisionError:
        currentWebbedSpeed = 0
    else:
        appliedMultipliers = {}
        # Modules first, they are applied always the same way
        for wData in webMods:
            appliedBoost = wData.boost * _calcRangeFactor(
                atkOptimalRange=wData.optimal,
                atkFalloffRange=wData.falloff,
                distance=distance)
            if appliedBoost:
                appliedMultipliers.setdefault(wData.stackingGroup, []).append((1 + appliedBoost / 100, wData.resAttrID))
        maxWebbedSpeed = tgt.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=appliedMultipliers)
        currentWebbedSpeed = maxWebbedSpeed * speedRatio
        # Drones and fighters
        mobileWebs = []
        mobileWebs.extend(webFighters)
        # Drones have range limit
        if distance <= fit.extraAttributes['droneControlRange']:
            mobileWebs.extend(webDrones)
        atkRadius = fit.ship.getModifiedItemAttr('radius')
        # As mobile webs either follow the target or stick to the attacking ship,
        # if target is within mobile web optimal - it can be applied unconditionally
        longEnoughMws = [mw for mw in mobileWebs if distance <= mw.optimal - atkRadius + mw.radius]
        if longEnoughMws:
            for mwData in longEnoughMws:
                appliedMultipliers.setdefault(mwData.stackingGroup, []).append((1 + mwData.boost / 100, mwData.resAttrID))
                mobileWebs.remove(mwData)
            maxWebbedSpeed = tgt.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=appliedMultipliers)
            currentWebbedSpeed = maxWebbedSpeed * speedRatio
        # Apply remaining webs, from fastest to slowest
        droneOpt = GraphSettings.getInstance().get('mobileDroneMode')
        while mobileWebs:
            # Process in batches unified by speed to save up resources
            fastestMwSpeed = max(mobileWebs, key=lambda mw: mw.speed).speed
            fastestMws = [mw for mw in mobileWebs if mw.speed == fastestMwSpeed]
            for mwData in fastestMws:
                # Faster than target or set to follow it - apply full slowdown
                if (droneOpt == GraphDpsDroneMode.auto and mwData.speed >= currentWebbedSpeed) or droneOpt == GraphDpsDroneMode.followTarget:
                    appliedMwBoost = mwData.boost
                # Otherwise project from the center of the ship
                else:
                    appliedMwBoost = mwData.boost * _calcRangeFactor(
                        atkOptimalRange=mwData.optimal,
                        atkFalloffRange=mwData.falloff,
                        distance=distance + atkRadius - mwData.radius)
                appliedMultipliers.setdefault(mwData.stackingGroup, []).append((1 + appliedMwBoost / 100, mwData.resAttrID))
                mobileWebs.remove(mwData)
            maxWebbedSpeed = tgt.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=appliedMultipliers)
            currentWebbedSpeed = maxWebbedSpeed * speedRatio
    return currentWebbedSpeed


def getTpMult(fit, tgt, tgtSpeed, tpMods, tpDrones, tpFighters, distance):
    if tgt.ship.getModifiedItemAttr('disallowOffensiveModifiers'):
        return 1
    untpedSig = tgt.ship.getModifiedItemAttr('signatureRadius')
    # Modules
    appliedMultipliers = {}
    for tpData in tpMods:
        appliedBoost = tpData.boost * _calcRangeFactor(
            atkOptimalRange=tpData.optimal,
            atkFalloffRange=tpData.falloff,
            distance=distance)
        if appliedBoost:
            appliedMultipliers.setdefault(tpData.stackingGroup, []).append((1 + appliedBoost / 100, tpData.resAttrID))
    # Drones and fighters
    mobileTps = []
    mobileTps.extend(tpFighters)
    # Drones have range limit
    if distance <= fit.extraAttributes['droneControlRange']:
        mobileTps.extend(tpDrones)
    droneOpt = GraphSettings.getInstance().get('mobileDroneMode')
    atkRadius = fit.ship.getModifiedItemAttr('radius')
    for mtpData in mobileTps:
        # Faster than target or set to follow it - apply full TP
        if (droneOpt == GraphDpsDroneMode.auto and mtpData.speed >= tgtSpeed) or droneOpt == GraphDpsDroneMode.followTarget:
            appliedMtpBoost = mtpData.boost
        # Otherwise project from the center of the ship
        else:
            appliedMtpBoost = mtpData.boost * _calcRangeFactor(
                atkOptimalRange=mtpData.optimal,
                atkFalloffRange=mtpData.falloff,
                distance=distance + atkRadius - mtpData.radius)
        appliedMultipliers.setdefault(mtpData.stackingGroup, []).append((1 + appliedMtpBoost / 100, mtpData.resAttrID))
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
