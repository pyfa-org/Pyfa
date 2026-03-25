import math
from bisect import bisect_right

from eos.calc import calculateRangeFactor
from eos.utils.float import floatUnerr
from graphs.calc import checkLockRange, checkDroneControlRange
from service.const import GraphDpsDroneMode
from service.settings import GraphSettings

from logbook import Logger

pyfalog = Logger(__name__)


# =============================================================================
# Re-exports from fitDamageStats for convenience
# =============================================================================

from graphs.data.fitDamageStats.calc.projected import (
    getScramRange,
    getScrammables,
    getTackledSpeed,
    getSigRadiusMult,
)


# =============================================================================
# Distance-Keyed Projected Cache
# =============================================================================

def buildProjectedCache(src, tgt, commonData, baseTgtSpeed, baseTgtSigRadius,
                        maxDistance=300000, resolution=100, existingCache=None):
    """
    Build a distance-keyed cache of target speed and signature radius.
    
    This pre-computes the expensive getTackledSpeed() and getSigRadiusMult()
    calls at regular intervals, allowing O(1) lookup during ammo optimization.
    
    If an existingCache is provided and the target hasn't changed (same base 
    speed/sig), we extend it rather than rebuild from scratch.
    
    Args:
        src: Source fit wrapper
        tgt: Target wrapper
        commonData: Dict with projected effect data (webMods, tpMods, etc.)
        baseTgtSpeed: Base (untackled) target speed
        baseTgtSigRadius: Base target signature radius
        maxDistance: Maximum distance to cache (m)
        resolution: Distance interval (m)
        existingCache: Optional existing cache to extend (if target unchanged)
    
    Returns:
        Dict with:
            'distances': sorted list of distance keys
            'cache': {distance: {'tgtSpeed': float, 'tgtSigRadius': float}}
            'hasProjected': bool - whether projected effects are applied
            'maxCachedDistance': int - highest distance in cache
    """
    applyProjected = commonData.get('applyProjected', False)
    
    # If no projected effects, return a simple cache with base values
    if not applyProjected:
        return {
            'distances': [],
            'cache': {},
            'hasProjected': False,
            'baseTgtSpeed': baseTgtSpeed,
            'baseTgtSigRadius': baseTgtSigRadius,
            'maxCachedDistance': 0
        }
    
    # Check if we can extend an existing cache
    # NOTE: Vector angles are now included in the projectedCacheKey (in getter.py)
    # so this cache is already isolated per vector configuration. We only need to
    # check if the base target parameters match.
    canExtend = (
        existingCache is not None and
        existingCache.get('hasProjected', False) and
        existingCache.get('baseTgtSpeed') == baseTgtSpeed and
        existingCache.get('baseTgtSigRadius') == baseTgtSigRadius
    )
    
    if canExtend:
        existingMax = existingCache.get('maxCachedDistance', 0)
        
        # If existing cache already covers our needed range, just return it
        if existingMax >= maxDistance:
            pyfalog.debug(f"[PROJECTED] Existing cache sufficient: {existingMax/1000:.0f}km >= {maxDistance/1000:.0f}km needed")
            return existingCache
        
        # Otherwise, extend the existing cache
        sigStr = 'inf' if baseTgtSigRadius == float('inf') else f"{baseTgtSigRadius:.1f}m"
        pyfalog.debug(f"[PROJECTED] Extending cache: {existingMax/1000:.0f}km -> {maxDistance/1000:.0f}km (baseSig={sigStr})")
        distances = existingCache['distances'].copy()
        cache = existingCache['cache'].copy()
        startDistance = existingMax + resolution
    else:
        sigStr = 'inf' if baseTgtSigRadius == float('inf') else f"{baseTgtSigRadius:.1f}m"
        distances = []
        cache = {}
        startDistance = 0
    
    # Extract projected data from commonData
    srcScramRange = commonData.get('srcScramRange', 0)
    tgtScrammables = commonData.get('tgtScrammables', ())
    webMods = commonData.get('webMods', ())
    webDrones = commonData.get('webDrones', ())
    webFighters = commonData.get('webFighters', ())
    tpMods = commonData.get('tpMods', ())
    tpDrones = commonData.get('tpDrones', ())
    tpFighters = commonData.get('tpFighters', ())
    
    # Debug log projected modules
    if webMods or webDrones or webFighters:
        pyfalog.debug(f"[PROJECTED] Webs: {len(webMods)} mods, {len(webDrones)} drones, {len(webFighters)} fighters")
    if tpMods or tpDrones or tpFighters:
        pyfalog.debug(f"[PROJECTED] TPs: {len(tpMods)} mods, {len(tpDrones)} drones, {len(tpFighters)} fighters")
    
    distance = startDistance
    entriesAdded = 0
    prevSpeed = None
    while distance <= maxDistance:
        # Calculate tackled speed at this distance
        tackledSpeed = getTackledSpeed(
            src=src,
            tgt=tgt,
            currentUntackledSpeed=baseTgtSpeed,
            srcScramRange=srcScramRange,
            tgtScrammables=tgtScrammables,
            webMods=webMods,
            webDrones=webDrones,
            webFighters=webFighters,
            distance=distance
        )
        
        # Calculate sig radius multiplier at this distance
        sigMult = getSigRadiusMult(
            src=src,
            tgt=tgt,
            tgtSpeed=tackledSpeed,
            srcScramRange=srcScramRange,
            tgtScrammables=tgtScrammables,
            tpMods=tpMods,
            tpDrones=tpDrones,
            tpFighters=tpFighters,
            distance=distance
        )
        
        # Log significant speed changes (helps debug grapple/web transitions)
        if prevSpeed is not None and abs(tackledSpeed - prevSpeed) > baseTgtSpeed * 0.05:
            pyfalog.debug(f"[PROJECTED] Speed change @ {distance/1000:.1f}km: {prevSpeed:.0f} -> {tackledSpeed:.0f} m/s")
        prevSpeed = tackledSpeed
        
        distances.append(distance)
        cache[distance] = {
            'tgtSpeed': tackledSpeed,
            'tgtSigRadius': baseTgtSigRadius * sigMult
        }
        
        distance += resolution
        entriesAdded += 1
    
    # Ensure distances list is sorted (should already be, but safe to ensure)
    distances.sort()
    
    return {
        'distances': distances,
        'cache': cache,
        'hasProjected': True,
        'baseTgtSpeed': baseTgtSpeed,
        'baseTgtSigRadius': baseTgtSigRadius,
        'maxCachedDistance': distances[-1] if distances else 0
    }


def getProjectedParamsAtDistance(projectedCache, distance, interpolate=True):
    """
    Get target speed and sig radius at a distance from the pre-built cache.
    
    Uses linear interpolation between cache entries for smoother curves,
    especially important for grapples/webs with falloff mechanics.
    
    Args:
        projectedCache: Cache dict from buildProjectedCache()
        distance: Distance to query (m)
        interpolate: If True, interpolate between cache entries (default)
    
    Returns:
        Dict with 'tgtSpeed' and 'tgtSigRadius'
    """
    if not projectedCache.get('hasProjected', False):
        # No projected effects - return base values
        return {
            'tgtSpeed': projectedCache.get('baseTgtSpeed', 0),
            'tgtSigRadius': projectedCache.get('baseTgtSigRadius', 0)
        }
    
    distances = projectedCache.get('distances', [])
    cache = projectedCache.get('cache', {})
    
    if not distances:
        return {
            'tgtSpeed': projectedCache.get('baseTgtSpeed', 0),
            'tgtSigRadius': projectedCache.get('baseTgtSigRadius', 0)
        }
    
    # Find position in sorted distances
    idx = bisect_right(distances, distance) - 1
    
    # Clamp to valid range
    if idx < 0:
        idx = 0
    if idx >= len(distances) - 1:
        # At or beyond the last cached distance
        distKey = distances[-1]
        return cache[distKey]
    
    # Get bounding distances
    distLow = distances[idx]
    distHigh = distances[idx + 1]
    
    # If not interpolating or exact match, return lower bound
    if not interpolate or distance <= distLow:
        return cache[distLow]
    
    # Linear interpolation
    cacheLow = cache[distLow]
    cacheHigh = cache[distHigh]
    
    # Calculate interpolation factor (0-1)
    t = (distance - distLow) / (distHigh - distLow) if distHigh > distLow else 0
    
    # Interpolate both speed and sig radius
    # Handle infinity properly - if either value is inf, result should be inf
    tgtSpeed = cacheLow['tgtSpeed'] + t * (cacheHigh['tgtSpeed'] - cacheLow['tgtSpeed'])
    if cacheLow['tgtSigRadius'] == float('inf') or cacheHigh['tgtSigRadius'] == float('inf'):
        tgtSigRadius = float('inf')
    else:
        tgtSigRadius = cacheLow['tgtSigRadius'] + t * (cacheHigh['tgtSigRadius'] - cacheLow['tgtSigRadius'])
    
    return {
        'tgtSpeed': tgtSpeed,
        'tgtSigRadius': tgtSigRadius
    }
