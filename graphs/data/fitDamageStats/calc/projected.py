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

from eos.utils.float import floatUnerr
from graphs.calc import calculateRangeFactor
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
    for mod in src.item.modules:
        if _isRegularScram(mod) or _isHicScram(mod):
            scramRange = max(scramRange or 0, mod.maxRange or 0)
    return scramRange


def getScrammables(tgt):
    scrammables = []
    if tgt.isFit:
        for mod in tgt.item.modules:
            if not mod.item:
                continue
            if {'moduleBonusMicrowarpdrive', 'microJumpDrive', 'microJumpPortalDrive'}.intersection(mod.item.effects):
                scrammables.append(mod)
    return scrammables


def getWebbedSpeed(src, tgt, currentUnwebbedSpeed, webMods, webDrones, webFighters, distance):
    # Can slow down non-immune ships and target profiles
    if tgt.isFit and tgt.item.ship.getModifiedItemAttr('disallowOffensiveModifiers'):
        return currentUnwebbedSpeed
    maxUnwebbedSpeed = tgt.getMaxVelocity()
    # What's immobile cannot be slowed
    if maxUnwebbedSpeed == 0:
        return maxUnwebbedSpeed
    speedRatio = currentUnwebbedSpeed / maxUnwebbedSpeed
    appliedMultipliers = {}
    # Modules first, they are applied always the same way
    for wData in webMods:
        appliedBoost = wData.boost * calculateRangeFactor(
            srcOptimalRange=wData.optimal,
            srcFalloffRange=wData.falloff,
            distance=distance)
        if appliedBoost:
            appliedMultipliers.setdefault(wData.stackingGroup, []).append((1 + appliedBoost / 100, wData.resAttrID))
    maxWebbedSpeed = tgt.getMaxVelocity(extraMultipliers=appliedMultipliers)
    currentWebbedSpeed = maxWebbedSpeed * speedRatio
    # Drones and fighters
    mobileWebs = []
    mobileWebs.extend(webFighters)
    # Drones have range limit
    if distance is None or distance <= src.item.extraAttributes['droneControlRange']:
        mobileWebs.extend(webDrones)
    atkRadius = src.getRadius()
    # As mobile webs either follow the target or stick to the attacking ship,
    # if target is within mobile web optimal - it can be applied unconditionally
    longEnoughMws = [mw for mw in mobileWebs if distance is None or distance <= mw.optimal - atkRadius + mw.radius]
    if longEnoughMws:
        for mwData in longEnoughMws:
            appliedMultipliers.setdefault(mwData.stackingGroup, []).append((1 + mwData.boost / 100, mwData.resAttrID))
            mobileWebs.remove(mwData)
        maxWebbedSpeed = tgt.getMaxVelocity(extraMultipliers=appliedMultipliers)
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
        maxWebbedSpeed = tgt.getMaxVelocity(extraMultipliers=appliedMultipliers)
        currentWebbedSpeed = maxWebbedSpeed * speedRatio
    # Ensure consistent results - round off a little to avoid float errors
    return floatUnerr(currentWebbedSpeed)


def getTpMult(src, tgt, tgtSpeed, tpMods, tpDrones, tpFighters, distance):
    # Can blow non-immune ships and target profiles
    if tgt.isFit and tgt.item.ship.getModifiedItemAttr('disallowOffensiveModifiers'):
        return 1
    untpedSig = tgt.getSigRadius()
    # Modules
    appliedMultipliers = {}
    for tpData in tpMods:
        appliedBoost = tpData.boost * calculateRangeFactor(
            srcOptimalRange=tpData.optimal,
            srcFalloffRange=tpData.falloff,
            distance=distance)
        if appliedBoost:
            appliedMultipliers.setdefault(tpData.stackingGroup, []).append((1 + appliedBoost / 100, tpData.resAttrID))
    # Drones and fighters
    mobileTps = []
    mobileTps.extend(tpFighters)
    # Drones have range limit
    if distance is None or distance <= src.item.extraAttributes['droneControlRange']:
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
    tpedSig = tgt.getSigRadius(extraMultipliers=appliedMultipliers)
    if tpedSig == math.inf and untpedSig == math.inf:
        return 1
    mult = tpedSig / untpedSig
    # Ensure consistent results - round off a little to avoid float errors
    return floatUnerr(mult)
