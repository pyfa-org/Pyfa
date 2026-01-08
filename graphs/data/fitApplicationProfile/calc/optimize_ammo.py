from bisect import bisect_right

from logbook import Logger

from .turret import calculateAppliedVolley
from .projected import getProjectedParamsAtDistance


pyfalog = Logger(__name__)


# =============================================================================
# Utility Functions
# =============================================================================

def volleyToDps(volley, cycleTimeMs):
    """
    Convert volley to DPS.
    
    Args:
        volley: Damage per shot
        cycleTimeMs: Cycle time in milliseconds
    
    Returns:
        DPS (damage per second)
    """
    if cycleTimeMs <= 0:
        return 0
    return volley / (cycleTimeMs / 1000)


# =============================================================================
# Best Charge Finding
# =============================================================================

def findBestCharge(chargeData, distance, turretBase, trackingParams):
    """
    Find the best charge at a distance based on applied volley.
    
    Args:
        chargeData: List of charge data dicts
        distance: Surface-to-surface distance (m)
        turretBase: Base turret stats dict
        trackingParams: Tracking params dict or None for perfect tracking
    
    Returns:
        Tuple of (best_volley, best_name, best_index)
    """
    bestVolley = 0
    bestName = None
    bestIndex = 0
    
    for i, cd in enumerate(chargeData):
        volley = calculateAppliedVolley(cd, distance, turretBase, trackingParams)
        if volley > bestVolley:
            bestVolley = volley
            bestName = cd['name']
            bestIndex = i
    
    return bestVolley, bestName, bestIndex


# =============================================================================
# Transition Point Calculation
# =============================================================================

def _updateTrackingWithCache(baseTrackingParams, projectedCache, distance):
    """
    Fast update of tracking params using pre-built projected cache.
    
    This is the performance-critical inner loop optimization - instead of
    calling getTackledSpeed/getSigRadiusMult 300+ times, we do a single
    cache lookup.
    
    Args:
        baseTrackingParams: Base tracking params dict (or None for perfect tracking)
        projectedCache: Cache from buildProjectedCache()
        distance: Distance (m)
    
    Returns:
        Updated tracking params dict with cached tgtSpeed/tgtSigRadius
    """
    if baseTrackingParams is None:
        return None
    
    params = baseTrackingParams.copy()
    projected = getProjectedParamsAtDistance(projectedCache, distance)
    params['tgtSpeed'] = projected['tgtSpeed']
    params['tgtSigRadius'] = projected['tgtSigRadius']
    return params


def calculateTransitions(chargeData, turretBase, baseTrackingParams,
                         projectedCache,
                         maxDistance=300000, resolution=100):
    """
    Calculate distances where optimal ammo changes.
    
    Uses coarse resolution for scanning, then binary search for exact 
    transition points. This is much faster than fine-grained scanning.
    
    PERFORMANCE: Uses projectedCache for O(1) lookup of target speed/sig
    at each distance, avoiding expensive getTackledSpeed/getSigRadiusMult calls.
    
    Args:
        chargeData: List of charge data dicts
        turretBase: Base turret stats dict
        baseTrackingParams: Base tracking params dict (with base tgtSpeed/tgtSigRadius)
        projectedCache: Pre-built cache from buildProjectedCache()
        maxDistance: Maximum distance to scan (m)
        resolution: Scan resolution (m)
    
    Returns:
        List of tuples: [(distance, charge_index, charge_name, volley), ...]
    """
    if not chargeData:
        return []
    
    transitions = []
    currentCharge = None
    
    # Start at distance 0
    params0 = _updateTrackingWithCache(baseTrackingParams, projectedCache, 0)
    bestVolley, bestName, bestIdx = findBestCharge(chargeData, 0, turretBase, params0)
    transitions.append((0, bestIdx, bestName, bestVolley))
    currentCharge = bestName
    
    # Scan for transitions
    distance = resolution
    while distance <= maxDistance:
        params = _updateTrackingWithCache(baseTrackingParams, projectedCache, distance)
        bestVolley, bestName, bestIdx = findBestCharge(chargeData, distance, turretBase, params)
        
        if bestName != currentCharge:
            # Binary search for exact transition point
            low, high = distance - resolution, distance
            while high - low > 10:
                mid = (low + high) // 2
                paramsMid = _updateTrackingWithCache(baseTrackingParams, projectedCache, mid)
                _, midName, _ = findBestCharge(chargeData, mid, turretBase, paramsMid)
                if midName == currentCharge:
                    low = mid
                else:
                    high = mid
            
            # Get volley at transition
            paramsHigh = _updateTrackingWithCache(baseTrackingParams, projectedCache, high)
            bestVolley, _, _ = findBestCharge(chargeData, high, turretBase, paramsHigh)
            
            transitions.append((high, bestIdx, bestName, bestVolley))
            currentCharge = bestName
        
        distance += resolution
    
    return transitions


# =============================================================================
# Query Functions
# =============================================================================

def getVolleyAtDistance(transitions, chargeData, turretBase, distance,
                        baseTrackingParams, projectedCache):
    """
    Get applied volley at a specific distance.
    
    Uses transitions for O(log n) charge lookup, then calculates exact volley
    using the pre-built projected cache for target speed/sig.
    
    Args:
        transitions: List of transition tuples from calculateTransitions
        chargeData: List of charge data dicts
        turretBase: Base turret stats dict
        distance: Distance to query (m)
        baseTrackingParams: Base tracking params dict
        projectedCache: Pre-built cache from buildProjectedCache()
    
    Returns:
        Tuple of (volley, charge_name)
    """
    if not transitions:
        return 0, None
    
    # Find which charge is optimal at this distance
    distances = [t[0] for t in transitions]
    idx = bisect_right(distances, distance) - 1
    if idx < 0:
        idx = 0
    
    chargeIdx = transitions[idx][1]
    cd = chargeData[chargeIdx]
    
    # Calculate exact volley with projected effects from cache
    params = _updateTrackingWithCache(baseTrackingParams, projectedCache, distance)
    volley = calculateAppliedVolley(cd, distance, turretBase, params)
    
    return volley, cd['name']
