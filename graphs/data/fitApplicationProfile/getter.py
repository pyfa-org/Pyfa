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

from eos.const import FittingHardpoint
from logbook import Logger

from graphs.data.base.getter import SmoothPointGetter
from graphs.data.fitDamageStats.calc.projected import (
    getScramRange, getScrammables
)
from service.settings import GraphSettings
from .calc.valid_charges import getValidChargesForModule

from .calc.turret import (
    getTurretBaseStats,
    getSkillMultiplier
)
from .calc.charges import (
    filterChargesByQuality,
    precomputeChargeData,
    getLongestRangeMultiplier
)
from .calc.optimize_ammo import (
    volleyToDps,
    calculateTransitions,
    getVolleyAtDistance
)
from .calc.projected import (
    buildProjectedCache,
    getSampleStep
)
from .calc.launcher import (
    getAllMultipliers as getLauncherMultipliers,
    precomputeMissileChargeData,
    getMaxEffectiveRange as getMissileMaxEffectiveRange,
    calculateTransitions as calculateMissileTransitions,
    getVolleyAtDistance as getMissileVolleyAtDistance,
    volleyToDps as missileVolleyToDps
)


pyfalog = Logger(__name__)


# =============================================================================
# Max Effective Range Calculation
# =============================================================================

def getMaxEffectiveRange(turretBase, charges):
    """
    Calculate the max effective range for a turret with its available charges.

    Formula: optimal * longestRangeMult + falloff * 3.1

    At falloff * 3.1, the range factor is ~0.5% (negligible damage).

    Args:
        turretBase: Base turret stats dict from getTurretBaseStats
        charges: List of charge items

    Returns:
        Max effective range in meters
    """
    longestRangeMult = getLongestRangeMultiplier(charges)
    effectiveOptimal = turretBase['optimal'] * longestRangeMult
    effectiveMaxRange = effectiveOptimal + turretBase['falloff'] * 3.1
    return int(effectiveMaxRange)


def getTurretRangeInfo(mod, qualityTier, chargeCache=None):
    """
    Get turret base stats and max effective range without computing transitions.

    This is used in the first pass to determine how far the projected cache
    needs to extend.

    Args:
        mod: The turret module
        qualityTier: 't1', 'navy', or 'all'
        chargeCache: Optional cache dict for getValidCharges results

    Returns:
        Dict with turret_base, charges, max_effective_range, cycle_time_ms
        Or None if turret has no valid charges
    """
    # Get turret base stats
    turretBase = getTurretBaseStats(mod)

    # Get cycle time
    cycleParams = mod.getCycleParameters()
    if cycleParams is None:
        return None
    cycleTimeMs = cycleParams.averageTime

    # Get and filter charges - use cache if available
    chargeCacheKey = (mod.item.ID, qualityTier)
    if chargeCache is not None and chargeCacheKey in chargeCache:
        charges = chargeCache[chargeCacheKey]
    else:
        allCharges = list(getValidChargesForModule(mod))
        charges = filterChargesByQuality(allCharges, qualityTier)
        if chargeCache is not None:
            chargeCache[chargeCacheKey] = charges

    if not charges:
        return None

    # Calculate max effective range
    maxEffectiveRange = getMaxEffectiveRange(turretBase, charges)

    return {
        'turret_base': turretBase,
        'charges': charges,
        'max_effective_range': maxEffectiveRange,
        'cycle_time_ms': cycleTimeMs
    }


# =============================================================================
# Launcher Max Range Functions
# =============================================================================

def getLauncherRangeInfo(mod, qualityTier, shipRadius, chargeCache=None):
    """
    Get launcher stats and max effective range without computing transitions.

    This is used in the first pass to determine how far the projected cache
    needs to extend.

    Args:
        mod: The launcher module
        qualityTier: 't1', 'navy', or 'all'
        shipRadius: Ship radius for flight time bonus
        chargeCache: Optional cache dict for getValidCharges results

    Returns:
        Dict with charges, max_effective_range, cycle_time_ms, and multipliers
        Or None if launcher has no valid charges
    """
    # Get cycle time
    cycleParams = mod.getCycleParameters()
    if cycleParams is None:
        return None
    cycleTimeMs = cycleParams.averageTime

    # Get and filter charges - use cache if available
    chargeCacheKey = (mod.item.ID, qualityTier)
    if chargeCache is not None and chargeCacheKey in chargeCache:
        charges = chargeCache[chargeCacheKey]
    else:
        allCharges = list(getValidChargesForModule(mod))
        charges = filterChargesByQuality(allCharges, qualityTier)
        if chargeCache is not None:
            chargeCache[chargeCacheKey] = charges

    if not charges:
        return None

    # Get multipliers from the currently loaded charge (or first valid charge)
    damageMults, flightMults, appMults = getLauncherMultipliers(mod)

    # Get launcher damage multiplier
    launcherDamageMult = mod.getModifiedItemAttr('damageMultiplier') or 1

    # Precompute charge data to determine max effective range
    chargeData = precomputeMissileChargeData(
        mod, charges, cycleTimeMs, shipRadius,
        damageMults, flightMults, appMults,
        tgtResists=None  # Don't filter by resists for range calculation
    )

    if not chargeData:
        return None

    # Max effective range is from the longest-range charge
    maxEffectiveRange = getMissileMaxEffectiveRange(chargeData)

    return {
        'charges': charges,
        'charge_data': chargeData,  # Cache the precomputed data
        'max_effective_range': maxEffectiveRange,
        'cycle_time_ms': cycleTimeMs,
        'damage_mults': damageMults,
        'flight_mults': flightMults,
        'app_mults': appMults,
        'launcher_damage_mult': launcherDamageMult
    }


# =============================================================================
# Dominant Group Detection
# =============================================================================

def countWeaponGroups(src):
    """
    Count turrets and launchers on the source fit.

    Args:
        src: Source fit wrapper

    Returns:
        Tuple of (turret_count, launcher_count)
    """
    turretCount = 0
    launcherCount = 0

    for mod in src.item.activeModulesIter():
        # Skip mining lasers
        if mod.getModifiedItemAttr('miningAmount'):
            continue

        if mod.hardpoint == FittingHardpoint.TURRET:
            turretCount += 1
        elif mod.hardpoint == FittingHardpoint.MISSILE:
            launcherCount += 1

    return turretCount, launcherCount


def getDominantWeaponType(src):
    """
    Determine which weapon type dominates on the fit.

    Args:
        src: Source fit wrapper

    Returns:
        'turret', 'launcher', or None (if no weapons)
    """
    turretCount, launcherCount = countWeaponGroups(src)

    if turretCount == 0 and launcherCount == 0:
        return None

    # Turrets win ties (arbitrary, but consistent)
    if turretCount >= launcherCount:
        return 'turret'
    else:
        return 'launcher'


# =============================================================================
# Cache Building
# =============================================================================

def buildTurretCacheEntry(mod, qualityTier, tgtResists, baseTrackingParams,
                          projectedCache, chargeCache=None, rangeInfo=None):
    """
    Build a complete cache entry for a single turret type.

    Args:
        mod: The turret module
        qualityTier: 't1', 'navy', or 'all'
        tgtResists: Target resists tuple or None
        baseTrackingParams: Base tracking params dict
        projectedCache: Pre-built cache from buildProjectedCache()
        chargeCache: Optional cache dict for getValidCharges results
        rangeInfo: Optional pre-computed range info from getTurretRangeInfo

    Returns:
        Dict with charge_data, transitions, turret_base, cycle_time_ms
        Or None if turret has no valid charges
    """
    # Use pre-computed range info if available, otherwise compute now
    if rangeInfo is not None:
        turretBase = rangeInfo['turret_base']
        charges = rangeInfo['charges']
        cycleTimeMs = rangeInfo['cycle_time_ms']
    else:
        turretBase = getTurretBaseStats(mod)
        cycleParams = mod.getCycleParameters()
        if cycleParams is None:
            return None
        cycleTimeMs = cycleParams.averageTime

        # Get and filter charges
        chargeCacheKey = (mod.item.ID, qualityTier)
        if chargeCache is not None and chargeCacheKey in chargeCache:
            charges = chargeCache[chargeCacheKey]
        else:
            allCharges = list(getValidChargesForModule(mod))
            charges = filterChargesByQuality(allCharges, qualityTier)
            if chargeCache is not None:
                chargeCache[chargeCacheKey] = charges

        if not charges:
            return None

    if not charges:
        return None

    # Get skill multiplier
    skillMult = getSkillMultiplier(mod)

    # Precompute charge data
    chargeData = precomputeChargeData(turretBase, charges, skillMult, tgtResists)

    # Calculate max effective range for this turret (after charge filtering)
    # Use the precomputed chargeData to get the longest range
    maxEffectiveOptimal = max(cd['effective_optimal'] for cd in chargeData)
    maxEffectiveFalloff = max(cd['effective_falloff'] for cd in chargeData)
    maxEffectiveRange = int(maxEffectiveOptimal + maxEffectiveFalloff * 3.1)

    # Calculate transitions using the pre-built projected cache
    # Only scan up to this turret's max effective range
    transitions = calculateTransitions(
        chargeData, turretBase, baseTrackingParams,
        projectedCache,
        maxDistance=maxEffectiveRange
    )

    return {
        'charge_data': chargeData,
        'transitions': transitions,
        'turret_base': turretBase,
        'cycle_time_ms': cycleTimeMs,
        'count': 1
    }


def buildLauncherCacheEntry(mod, qualityTier, tgtResists, shipRadius,
                            baseTgtSpeed, baseTgtSigRadius,
                            projectedCache, chargeCache=None, rangeInfo=None):
    """
    Build a complete cache entry for a single launcher type.


    Args:
        mod: The launcher module
        qualityTier: 't1', 'navy', or 'all'
        tgtResists: Target resists tuple or None
        shipRadius: Ship radius for flight time bonus
        baseTgtSpeed: Base target speed (from params)
        baseTgtSigRadius: Base target sig radius
        projectedCache: Pre-built cache from buildProjectedCache()
        chargeCache: Optional cache dict for getValidCharges results
        rangeInfo: Optional pre-computed range info from getLauncherRangeInfo

    Returns:
        Dict with charge_data, transitions, cycle_time_ms
        Or None if launcher has no valid charges
    """
    # Use pre-computed range info if available, otherwise compute now
    if rangeInfo is not None:
        charges = rangeInfo['charges']
        # chargeData = rangeInfo['charge_data']  # Don't use cached data (it ignores resists)
        cycleTimeMs = rangeInfo['cycle_time_ms']
        damageMults = rangeInfo['damage_mults']
        flightMults = rangeInfo['flight_mults']
        appMults = rangeInfo['app_mults']
    else:
        cycleParams = mod.getCycleParameters()
        if cycleParams is None:
            return None
        cycleTimeMs = cycleParams.averageTime

        # Get and filter charges
        chargeCacheKey = (mod.item.ID, qualityTier)
        if chargeCache is not None and chargeCacheKey in chargeCache:
            charges = chargeCache[chargeCacheKey]
        else:
            allCharges = list(getValidChargesForModule(mod))
            charges = filterChargesByQuality(allCharges, qualityTier)
            if chargeCache is not None:
                chargeCache[chargeCacheKey] = charges

        if not charges:
            return None

        # Get multipliers from the currently loaded charge
        damageMults, flightMults, appMults = getLauncherMultipliers(mod)

    # Precompute charge data with current resists
    chargeData = precomputeMissileChargeData(
        mod, charges, cycleTimeMs, shipRadius,
        damageMults, flightMults, appMults, tgtResists
    )

    if not chargeData:
        return None

    # Calculate max effective range from precomputed data
    maxEffectiveRange = getMissileMaxEffectiveRange(chargeData)

    # Calculate transitions using the pre-built projected cache
    transitions = calculateMissileTransitions(
        chargeData, baseTgtSpeed, baseTgtSigRadius,
        projectedCache,
        maxDistance=int(maxEffectiveRange)
    )

    return {
        'charge_data': chargeData,
        'transitions': transitions,
        'cycle_time_ms': cycleTimeMs,
        'count': 1
    }


# =============================================================================
# Y-Axis Mixins
# =============================================================================

class YOptimalAmmoDpsMixin:
    """Y-axis mixin: Calculate DPS using optimal ammo selection."""

    def _getOptimalDpsAtDistance(self, distance, weaponCache, trackingParams, projectedCache, weaponType):
        """Get total DPS with optimal ammo at a specific distance."""
        totalDps = 0

        if weaponType == 'turret':
            for group_id, groupInfo in weaponCache.items():
                volley, _ = getVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    groupInfo['turret_base'],
                    distance,
                    trackingParams,
                    projectedCache
                )
                dps = volleyToDps(volley, groupInfo['cycle_time_ms'])
                totalDps += dps * groupInfo['count']
        else:  # launcher
            tgtSpeed, tgtSigRadius = self._missileTargetParams(trackingParams)
            for group_id, groupInfo in weaponCache.items():
                volley, _ = getMissileVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    distance,
                    tgtSpeed,
                    tgtSigRadius,
                    projectedCache
                )
                dps = missileVolleyToDps(volley, groupInfo['cycle_time_ms'])
                totalDps += dps * groupInfo['count']

        return totalDps

    def _getOptimalDpsWithAmmoAtDistance(self, distance, weaponCache, trackingParams, projectedCache, weaponType):
        """Get total DPS and ammo name at a specific distance."""
        totalDps = 0
        ammoName = None

        if weaponType == 'turret':
            for groupInfo in weaponCache.values():
                volley, name = getVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    groupInfo['turret_base'],
                    distance,
                    trackingParams,
                    projectedCache
                )
                dps = volleyToDps(volley, groupInfo['cycle_time_ms'])
                totalDps += dps * groupInfo['count']
                if ammoName is None:
                    ammoName = name
        else:  # launcher
            tgtSpeed, tgtSigRadius = self._missileTargetParams(trackingParams)
            for groupInfo in weaponCache.values():
                volley, name = getMissileVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    distance,
                    tgtSpeed,
                    tgtSigRadius,
                    projectedCache
                )
                dps = missileVolleyToDps(volley, groupInfo['cycle_time_ms'])
                totalDps += dps * groupInfo['count']
                if ammoName is None:
                    ammoName = name

        return totalDps, ammoName


class YOptimalAmmoVolleyMixin:
    """Y-axis mixin: Calculate volley using optimal ammo selection."""

    def _getOptimalVolleyAtDistance(self, distance, weaponCache, trackingParams, projectedCache, weaponType):
        """Get total volley with optimal ammo at a specific distance."""
        totalVolley = 0

        if weaponType == 'turret':
            for groupInfo in weaponCache.values():
                volley, _ = getVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    groupInfo['turret_base'],
                    distance,
                    trackingParams,
                    projectedCache
                )
                totalVolley += volley * groupInfo['count']
        else:  # launcher
            tgtSpeed, tgtSigRadius = self._missileTargetParams(trackingParams)
            for groupInfo in weaponCache.values():
                volley, _ = getMissileVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    distance,
                    tgtSpeed,
                    tgtSigRadius,
                    projectedCache
                )
                totalVolley += volley * groupInfo['count']

        return totalVolley

    def _getOptimalVolleyWithAmmoAtDistance(self, distance, weaponCache, trackingParams, projectedCache, weaponType):
        """Get total volley and ammo name at a specific distance."""
        totalVolley = 0
        ammoName = None

        if weaponType == 'turret':
            for groupInfo in weaponCache.values():
                volley, name = getVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    groupInfo['turret_base'],
                    distance,
                    trackingParams,
                    projectedCache
                )
                totalVolley += volley * groupInfo['count']
                if ammoName is None:
                    ammoName = name
        else:  # launcher
            tgtSpeed, tgtSigRadius = self._missileTargetParams(trackingParams)
            for groupInfo in weaponCache.values():
                volley, name = getMissileVolleyAtDistance(
                    groupInfo['transitions'],
                    groupInfo['charge_data'],
                    distance,
                    tgtSpeed,
                    tgtSigRadius,
                    projectedCache
                )
                totalVolley += volley * groupInfo['count']
                if ammoName is None:
                    ammoName = name

        return totalVolley, ammoName


# =============================================================================
# X-Axis Mixin
# =============================================================================

class XDistanceMixin(SmoothPointGetter):
    """X-axis mixin: Distance in meters. Builds weapon cache and handles lookups."""

    # Coarse resolution for graph display - 100m intervals
    # Exact calculations are done on-demand via getPoint/getPointExtended
    _baseResolution = 100  # meters

    def _getCommonData(self, miscParams, src, tgt):
        """
        Build common data including projected cache and weapon (turret/launcher) cache.

        The projected cache is keyed by target (tgtSpeed, tgtSigRadius) and can be
        extended if the attacker's max range increases, without recalculating
        existing entries.
        """
        # Get settings
        qualityTier = getattr(self.graph, '_ammoQuality', 'all')
        ignoreResists = GraphSettings.getInstance().get('ammoOptimalIgnoreResists')
        applyProjected = GraphSettings.getInstance().get('ammoOptimalApplyProjected')

        tgtResists = None if (ignoreResists or tgt is None) else tgt.getResists()
        tgtSpeed = miscParams.get('tgtSpeed', 0) or 0
        tgtSigRadius = tgt.getSigRadius() if tgt else 0
        shipRadius = src.getRadius()

        weaponType = getDominantWeaponType(src)

        fit_id = src.item.ID

        atkSpeed = miscParams.get('atkSpeed', 0) or 0
        atkAngle = miscParams.get('atkAngle', 0) or 0
        tgtAngle = miscParams.get('tgtAngle', 0) or 0

        weaponCacheKey = (fit_id, weaponType, qualityTier, tgtResists, applyProjected, tgtSpeed, tgtSigRadius, atkSpeed, atkAngle, tgtAngle)

        projectedCacheKey = (fit_id, tgtSpeed, tgtSigRadius, atkSpeed, atkAngle, tgtAngle)

        # Initialize graph caches if needed
        if not hasattr(self.graph, '_ammo_weapon_cache'):
            self.graph._ammo_weapon_cache = {}
        if not hasattr(self.graph, '_ammo_charge_cache'):
            self.graph._ammo_charge_cache = {}
        if not hasattr(self.graph, '_ammo_projected_cache'):
            self.graph._ammo_projected_cache = {}

        # Build base commonData with projected effect info
        commonData = {
            'applyProjected': applyProjected,
            'src_radius': shipRadius,
            'weapon_type': weaponType,
        }

        # Add projected effect data if enabled
        if applyProjected:
            commonData['srcScramRange'] = getScramRange(src=src)
            commonData['tgtScrammables'] = getScrammables(tgt=tgt) if tgt else ()
            webMods, tpMods = self.graph._projectedCache.getProjModData(src)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(src)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(src)
            commonData['webMods'] = webMods
            commonData['tpMods'] = tpMods
            commonData['webDrones'] = webDrones
            commonData['tpDrones'] = tpDrones
            commonData['webFighters'] = webFighters
            commonData['tpFighters'] = tpFighters

        if weaponCacheKey in self.graph._ammo_weapon_cache:
            cached_weapon = self.graph._ammo_weapon_cache[weaponCacheKey]
            commonData['weapon_cache'] = cached_weapon
            commonData['projected_cache'] = self.graph._ammo_projected_cache.get(projectedCacheKey, {})
            return commonData

        if weaponType is None:
            commonData['weapon_cache'] = {}
            commonData['projected_cache'] = {}
            return commonData


        weaponRangeInfos = {}  # {mod.item.ID: rangeInfo}
        maxEffectiveRange = 0

        if weaponType == 'turret':
            hardpointType = FittingHardpoint.TURRET
        else:
            hardpointType = FittingHardpoint.MISSILE

        for mod in src.item.activeModulesIter():
            if mod.hardpoint != hardpointType:
                continue
            if mod.getModifiedItemAttr('miningAmount'):
                continue

            key = mod.item.ID
            if key not in weaponRangeInfos:
                if weaponType == 'turret':
                    rangeInfo = getTurretRangeInfo(mod, qualityTier, self.graph._ammo_charge_cache)
                else:
                    # Special handling for empty launchers (Missiles only):
                    # To apply skill/ship modifiers correctly, eos needs a charge loaded.
                    # If launcher is empty, temporarily load a charge to extract multipliers.
                    if mod.charge is None:
                        # Find a valid charge to simulate load
                        chargeCacheKey = (mod.item.ID, qualityTier)
                        validCharges = None
                        if self.graph._ammo_charge_cache is not None and chargeCacheKey in self.graph._ammo_charge_cache:
                             validCharges = self.graph._ammo_charge_cache[chargeCacheKey]

                        if validCharges is None:
                            allCharges = list(getValidChargesForModule(mod))
                            validCharges = filterChargesByQuality(allCharges, qualityTier)
                            if self.graph._ammo_charge_cache is not None:
                                self.graph._ammo_charge_cache[chargeCacheKey] = validCharges

                        if validCharges:
                            # Temporarily load the first valid charge
                            tempCharge = validCharges[0]
                            try:
                                mod.charge = tempCharge
                                # Force fit update (important for effects to apply)
                                if mod.owner:
                                    mod.owner.calculated = False
                                    mod.owner.calculateModifiedAttributes()

                                ranges = getLauncherRangeInfo(mod, qualityTier, shipRadius, self.graph._ammo_charge_cache)
                                rangeInfo = ranges

                                # Unload charge
                                mod.charge = None
                                if mod.owner:
                                    mod.owner.calculated = False
                                    mod.owner.calculateModifiedAttributes()

                            except Exception as e:
                                pyfalog.error(f"Error simulating charge for {mod.item.name}: {e}")
                                mod.charge = None # Ensure cleanup
                                if mod.owner:
                                    mod.owner.calculated = False
                                    try:
                                        mod.owner.calculateModifiedAttributes()
                                    except:
                                        pass
                                rangeInfo = None
                        else:
                            rangeInfo = None
                    else:
                        rangeInfo = getLauncherRangeInfo(mod, qualityTier, shipRadius, self.graph._ammo_charge_cache)

                if rangeInfo:
                    weaponRangeInfos[key] = rangeInfo
                    if rangeInfo['max_effective_range'] > maxEffectiveRange:
                        maxEffectiveRange = rangeInfo['max_effective_range']

        if not weaponRangeInfos:
            # No weapons found
            commonData['weapon_cache'] = {}
            commonData['projected_cache'] = {}
            return commonData

        # =====================================================================
        # PHASE 2: Build/extend projected cache to max effective range
        # =====================================================================

        # Get existing cache for this target (if any)
        existingCache = self.graph._ammo_projected_cache.get(projectedCacheKey)

        # Build base tracking params (used for turrets, also provides tgtSpeed/tgtSig for missiles)
        # Vector parameters already extracted above for cache keys
        baseTrackingParams = {
            'atkSpeed': atkSpeed,
            'atkAngle': atkAngle,
            'atkRadius': shipRadius,
            'tgtSpeed': tgtSpeed,
            'tgtAngle': tgtAngle,
            'tgtRadius': tgt.getRadius() if tgt else 0,
            'tgtSigRadius': tgtSigRadius
        }

        # Build or extend the projected cache
        projectedCache = buildProjectedCache(
            src=src,
            tgt=tgt,
            commonData=commonData,
            baseTgtSpeed=tgtSpeed,
            baseTgtSigRadius=tgtSigRadius,
            maxDistance=maxEffectiveRange,
            resolution=getSampleStep(maxEffectiveRange),
            existingCache=existingCache
        )

        # Store projected cache - can be reused if target stays the same
        self.graph._ammo_projected_cache[projectedCacheKey] = projectedCache
        commonData['projected_cache'] = projectedCache

        # =====================================================================
        # PHASE 3: Build weapon cache with transitions
        # =====================================================================

        weaponCache = {}
        for mod in src.item.activeModulesIter():
            if mod.hardpoint != hardpointType:
                continue
            if mod.getModifiedItemAttr('miningAmount'):
                continue

            key = mod.item.ID
            if key not in weaponCache:
                rangeInfo = weaponRangeInfos.get(key)
                if rangeInfo:
                    if weaponType == 'turret':
                        entry = buildTurretCacheEntry(
                            mod, qualityTier, tgtResists, baseTrackingParams,
                            projectedCache, self.graph._ammo_charge_cache,
                            rangeInfo=rangeInfo
                        )
                    else:
                        entry = buildLauncherCacheEntry(
                            mod, qualityTier, tgtResists, shipRadius,
                            tgtSpeed, tgtSigRadius,
                            projectedCache, self.graph._ammo_charge_cache,
                            rangeInfo=rangeInfo
                        )
                    if entry:
                        weaponCache[key] = entry
            else:
                weaponCache[key]['count'] += 1

        # Cache and return
        self.graph._ammo_weapon_cache[weaponCacheKey] = weaponCache
        commonData['weapon_cache'] = weaponCache

        return commonData

    def _buildTrackingParams(self, distance, miscParams, src, tgt, commonData):
        """
        Build base tracking params for a distance query.

        NOTE: This returns BASE params only. The projected effects (web/TP)
        are applied via the projected cache in getVolleyAtDistance.
        """
        tgtSpeed = miscParams.get('tgtSpeed', 0) or 0
        tgtSigRadius = tgt.getSigRadius() if tgt else 0

        # Only return None if sig radius is exactly 0 (not infinity - that's valid for Ideal Target)
        if tgtSigRadius == 0:
            return None

        params = {
            'atkSpeed': miscParams.get('atkSpeed', 0) or 0,
            'atkAngle': miscParams.get('atkAngle', 0) or 0,
            'atkRadius': commonData.get('src_radius', 0),
            'tgtSpeed': tgtSpeed,
            'tgtAngle': miscParams.get('tgtAngle', 0) or 0,
            'tgtRadius': tgt.getRadius() if tgt else 0,
            'tgtSigRadius': tgtSigRadius
        }

        return params

    @staticmethod
    def _missileTargetParams(trackingParams):
        """
        Extract (tgtSpeed, tgtSigRadius) for the missile volley calc from a
        possibly-None trackingParams.

        _buildTrackingParams returns None to mean "perfect tracking" (no target
        or a target with signature radius 0). The turret path mirrors this as a
        tracking factor of 1.0; for missiles we get the same full-application
        result by feeding an effectively-infinite signature (and zero speed)
        into the application formula. Without this guard the launcher branches
        raise TypeError subscripting None.
        """
        if trackingParams is None:
            return 0, float('inf')
        return trackingParams['tgtSpeed'], trackingParams['tgtSigRadius']

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        """Calculate value at distance x."""
        weaponCache = commonData.get('weapon_cache', {})
        weaponType = commonData.get('weapon_type')
        if not weaponCache:
            return 0

        trackingParams = self._buildTrackingParams(x, miscParams, src, tgt, commonData)
        projectedCache = commonData.get('projected_cache', {})

        if hasattr(self, '_getOptimalDpsAtDistance'):
            result = self._getOptimalDpsAtDistance(x, weaponCache, trackingParams, projectedCache, weaponType)
            return result
        elif hasattr(self, '_getOptimalVolleyAtDistance'):
            result = self._getOptimalVolleyAtDistance(x, weaponCache, trackingParams, projectedCache, weaponType)
            return result
        return 0

    def _calculatePointExtended(self, x, miscParams, src, tgt, commonData):
        """Calculate value and ammo name at distance x."""
        weaponCache = commonData.get('weapon_cache', {})
        weaponType = commonData.get('weapon_type')
        if not weaponCache:
            return 0, None

        trackingParams = self._buildTrackingParams(x, miscParams, src, tgt, commonData)
        projectedCache = commonData.get('projected_cache', {})

        if hasattr(self, '_getOptimalDpsWithAmmoAtDistance'):
            return self._getOptimalDpsWithAmmoAtDistance(x, weaponCache, trackingParams, projectedCache, weaponType)
        elif hasattr(self, '_getOptimalVolleyWithAmmoAtDistance'):
            return self._getOptimalVolleyWithAmmoAtDistance(x, weaponCache, trackingParams, projectedCache, weaponType)
        return 0, None

    def getSegments(self, xRange, miscParams, src, tgt):
        """Get plot segments with ammo transition information."""
        # Validate xRange - can contain None from range limiters
        minX, maxX = xRange
        if minX is None or maxX is None:
            return []

        commonData = self._getCommonData(miscParams=miscParams, src=src, tgt=tgt)
        weaponCache = commonData.get('weapon_cache', {})
        weaponType = commonData.get('weapon_type')

        if not weaponCache:
            return []

        # Get transitions from first weapon group
        transitions = None
        for groupInfo in weaponCache.values():
            transitions = groupInfo['transitions']
            break

        if not transitions:
            return []

        # Filter valid transitions (with ammo name)
        validTransitions = [t for t in transitions if t[2] is not None]
        if not validTransitions:
            return []

        # Build ammo index mapping
        ammoToIndex = {}
        for t in validTransitions:
            if t[2] not in ammoToIndex:
                ammoToIndex[t[2]] = len(ammoToIndex)

        # Generate segments
        segments = []

        # Scale plotting resolution with the visible range so long-range fits
        # don't sample thousands of points (falls back to 100m for short ranges).
        step = getSampleStep(maxX - minX)

        for i, transition in enumerate(validTransitions):
            transDist, _, ammoName, _ = transition
            segStart = max(transDist, minX)

            # Find segment end
            if i + 1 < len(validTransitions):
                segEnd = min(validTransitions[i + 1][0], maxX)
            else:
                segEnd = maxX

            if segStart >= segEnd:
                continue

            # Generate points at the range-scaled resolution for performance
            xs, ys = [], []
            x = segStart
            while x <= segEnd:
                y = self._calculatePoint(x, miscParams, src, tgt, commonData)
                xs.append(x)
                ys.append(y)
                x += step

            # Always include the segment end point for smooth transitions
            if xs[-1] < segEnd:
                y = self._calculatePoint(segEnd, miscParams, src, tgt, commonData)
                xs.append(segEnd)
                ys.append(y)

            segments.append({
                'xs': xs,
                'ys': ys,
                'ammo': ammoName,
                'ammoIndex': ammoToIndex[ammoName]
            })

        return segments


# =============================================================================
# Getter Classes
# =============================================================================

class Distance2OptimalAmmoDpsGetter(XDistanceMixin, YOptimalAmmoDpsMixin):
    """Distance vs Optimal Ammo DPS graph getter."""

    def getPointExtended(self, x, miscParams, src, tgt):
        commonData = self._getCommonData(miscParams=miscParams, src=src, tgt=tgt)
        value, ammo = self._calculatePointExtended(x, miscParams, src, tgt, commonData)
        return value, {'ammo': ammo}


class Distance2OptimalAmmoVolleyGetter(XDistanceMixin, YOptimalAmmoVolleyMixin):
    """Distance vs Optimal Ammo Volley graph getter."""

    def getPointExtended(self, x, miscParams, src, tgt):
        commonData = self._getCommonData(miscParams=miscParams, src=src, tgt=tgt)
        value, ammo = self._calculatePointExtended(x, miscParams, src, tgt, commonData)
        return value, {'ammo': ammo}
