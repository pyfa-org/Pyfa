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
from bisect import bisect_right

from eos.calc import calculateRangeFactor
from eos.utils.float import floatUnerr
from graphs.calc import checkLockRange, checkDroneControlRange
from service.const import GraphDpsDroneMode
from service.settings import GraphSettings


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
# Distance Sample Step
# =============================================================================

def getSampleStep(maxDistance, minStep=100, targetPoints=300):
    """
    Pick a distance-scan step that scales with the range being scanned.

    Several hot loops (ammo transition scanning, segment plotting) sample the
    curve at a fixed interval from 0 to the fit's max effective range. With a
    hardcoded step, cost grows linearly with range - a 250km fit does 25x the
    work of a 10km fit for no extra visual fidelity.

    This keeps the fine step for short-range fits (no accuracy change for the
    common case) and coarsens it for long-range fits so the number of sampled
    points stays roughly bounded by targetPoints.

    Args:
        maxDistance: Range to be scanned (m)
        minStep: Finest step; also the step used for short ranges (m)
        targetPoints: Approximate upper bound on the number of scan points

    Returns:
        Step size in meters (always a multiple of minStep, >= minStep)
    """
    if not maxDistance or maxDistance <= 0:
        return minStep
    step = maxDistance / targetPoints
    if step <= minStep:
        return minStep
    # Round up to a multiple of minStep so steps stay on tidy boundaries
    return int(math.ceil(step / minStep) * minStep)


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
            return existingCache

        # Otherwise, extend the existing cache
        distances = existingCache['distances'].copy()
        cache = existingCache['cache'].copy()
        startDistance = existingMax + resolution
    else:
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

    distance = startDistance
    entriesAdded = 0
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
