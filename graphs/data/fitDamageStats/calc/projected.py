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

from eos.calc import calculateRangeFactor
from eos.utils.float import floatUnerr
from graphs.calc import checkLockRange, checkDroneControlRange
from service.const import GraphDpsDroneMode
from service.settings import GraphSettings


def _isRegularScram(mod):
    if not mod.item:
        return False
    if not {'warpScrambleBlockMWDWithNPCEffect', 'structureWarpScrambleBlockMWDWithNPCEffect'}.intersection(mod.item.effects):
        return False
    if not mod.getModifiedItemAttr('activationBlockedStrenght', 0):
        return False
    return True


def _isHicScram(mod):
    if not mod.item:
        return False
    if 'warpDisruptSphere' not in mod.item.effects:
        return False
    if not mod.charge:
        return False
    if 'shipModuleFocusedWarpScramblingScript' not in mod.charge.effects:
        return False
    return True


def getScramRange(src):
    scramRange = None
    for mod in src.item.activeModulesIter():
        if _isRegularScram(mod) or _isHicScram(mod):
            scramRange = max(scramRange or 0, mod.maxRange or 0)
    return scramRange


def getScrammables(tgt):
    scrammables = []
    if tgt.isFit:
        for mod in tgt.item.activeModulesIter():
            if not mod.item:
                continue
            if {'moduleBonusMicrowarpdrive', 'microJumpDrive', 'microJumpPortalDrive'}.intersection(mod.item.effects):
                scrammables.append(mod)
    return scrammables


def getTackledSpeed(src, tgt, currentUntackledSpeed, srcScramRange, tgtScrammables, webMods, webDrones, webFighters, distance):
    # Can slow down non-immune ships and target profiles
    if tgt.isFit and tgt.item.ship.getModifiedItemAttr('disallowOffensiveModifiers'):
        return currentUntackledSpeed
    maxUntackledSpeed = tgt.getMaxVelocity()
    # What's immobile cannot be slowed
    if maxUntackledSpeed == 0:
        return maxUntackledSpeed
    inLockRange = checkLockRange(src=src, distance=distance)
    inDroneRange = checkDroneControlRange(src=src, distance=distance)
    speedRatio = currentUntackledSpeed / maxUntackledSpeed
    # No scrams or distance is longer than longest scram - nullify scrammables list
    if not inLockRange or srcScramRange is None or (distance is not None and distance > srcScramRange):
        tgtScrammables = ()
    appliedMultipliers = {}
    # Modules first, they are always applied the same way
    if inLockRange:
        for wData in webMods:
            appliedBoost = wData.boost * calculateRangeFactor(
                srcOptimalRange=wData.optimal,
                srcFalloffRange=wData.falloff,
                distance=distance)
            if appliedBoost:
                appliedMultipliers.setdefault(wData.stackingGroup, []).append((1 + appliedBoost / 100, wData.resAttrID))
    maxTackledSpeed = tgt.getMaxVelocity(extraMultipliers=appliedMultipliers, ignoreAfflictors=tgtScrammables)
    currentTackledSpeed = maxTackledSpeed * speedRatio
    # Drones and fighters
    mobileWebs = []
    if inLockRange:
        mobileWebs.extend(webFighters)
    if inLockRange and inDroneRange:
        mobileWebs.extend(webDrones)
    atkRadius = src.getRadius()
    # As mobile webs either follow the target or stick to the attacking ship,
    # if target is within mobile web optimal - it can be applied unconditionally
    longEnoughMws = [mw for mw in mobileWebs if distance is None or distance <= mw.optimal - atkRadius + mw.radius]
    if longEnoughMws:
        for mwData in longEnoughMws:
            appliedMultipliers.setdefault(mwData.stackingGroup, []).append((1 + mwData.boost / 100, mwData.resAttrID))
            mobileWebs.remove(mwData)
        maxTackledSpeed = tgt.getMaxVelocity(extraMultipliers=appliedMultipliers, ignoreAfflictors=tgtScrammables)
        currentTackledSpeed = maxTackledSpeed * speedRatio
    # Apply remaining webs, from fastest to slowest
    droneOpt = GraphSettings.getInstance().get('mobileDroneMode')
    while mobileWebs:
        # Process in batches unified by speed to save up resources
        fastestMwSpeed = max(mobileWebs, key=lambda mw: mw.speed).speed
        fastestMws = [mw for mw in mobileWebs if mw.speed == fastestMwSpeed]
        for mwData in fastestMws:
            # Faster than target or set to follow it - apply full slowdown
            if (droneOpt == GraphDpsDroneMode.auto and mwData.speed >= currentTackledSpeed) or droneOpt == GraphDpsDroneMode.followTarget:
                appliedMwBoost = mwData.boost
            # Otherwise project from the center of the ship
            else:
                if distance is None:
                    rangeFactorDistance = None
                else:
                    rangeFactorDistance = distance + atkRadius - mwData.radius
                appliedMwBoost = mwData.boost * calculateRangeFactor(
                    srcOptimalRange=mwData.optimal,
                    srcFalloffRange=mwData.falloff,
                    distance=rangeFactorDistance)
            appliedMultipliers.setdefault(mwData.stackingGroup, []).append((1 + appliedMwBoost / 100, mwData.resAttrID))
            mobileWebs.remove(mwData)
        maxTackledSpeed = tgt.getMaxVelocity(extraMultipliers=appliedMultipliers, ignoreAfflictors=tgtScrammables)
        currentTackledSpeed = maxTackledSpeed * speedRatio
    # Ensure consistent results - round off a little to avoid float errors
    return floatUnerr(currentTackledSpeed)


def getSigRadiusMult(src, tgt, tgtSpeed, srcScramRange, tgtScrammables, tpMods, tpDrones, tpFighters, distance):
    # Can blow non-immune ships and target profiles
    if tgt.isFit and tgt.item.ship.getModifiedItemAttr('disallowOffensiveModifiers'):
        return 1
    inLockRange = checkLockRange(src=src, distance=distance)
    inDroneRange = checkDroneControlRange(src=src, distance=distance)
    initSig = tgt.getSigRadius()
    # No scrams or distance is longer than longest scram - nullify scrammables list
    if not inLockRange or srcScramRange is None or (distance is not None and distance > srcScramRange):
        tgtScrammables = ()
    # TPing modules
    appliedMultipliers = {}
    if inLockRange:
        for tpData in tpMods:
            appliedBoost = tpData.boost * calculateRangeFactor(
                srcOptimalRange=tpData.optimal,
                srcFalloffRange=tpData.falloff,
                distance=distance)
            if appliedBoost:
                appliedMultipliers.setdefault(tpData.stackingGroup, []).append((1 + appliedBoost / 100, tpData.resAttrID))
    # TPing drones
    mobileTps = []
    if inLockRange:
        mobileTps.extend(tpFighters)
    if inLockRange and inDroneRange:
        mobileTps.extend(tpDrones)
    droneOpt = GraphSettings.getInstance().get('mobileDroneMode')
    atkRadius = src.getRadius()
    for mtpData in mobileTps:
        # Faster than target or set to follow it - apply full TP
        if (droneOpt == GraphDpsDroneMode.auto and mtpData.speed >= tgtSpeed) or droneOpt == GraphDpsDroneMode.followTarget:
            appliedMtpBoost = mtpData.boost
        # Otherwise project from the center of the ship
        else:
            if distance is None:
                rangeFactorDistance = None
            else:
                rangeFactorDistance = distance + atkRadius - mtpData.radius
            appliedMtpBoost = mtpData.boost * calculateRangeFactor(
                srcOptimalRange=mtpData.optimal,
                srcFalloffRange=mtpData.falloff,
                distance=rangeFactorDistance)
        appliedMultipliers.setdefault(mtpData.stackingGroup, []).append((1 + appliedMtpBoost / 100, mtpData.resAttrID))
    modifiedSig = tgt.getSigRadius(extraMultipliers=appliedMultipliers, ignoreAfflictors=tgtScrammables)
    if modifiedSig == math.inf and initSig == math.inf:
        return 1
    mult = modifiedSig / initSig
    # Ensure consistent results - round off a little to avoid float errors
    return floatUnerr(mult)
