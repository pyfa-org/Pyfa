import math
from bisect import bisect_right

from logbook import Logger

from .projected import getProjectedParamsAtDistance


pyfalog = Logger(__name__)


# =============================================================================
# Missile Application Factor
# =============================================================================

def calcMissileFactor(atkEr, atkEv, atkDrf, tgtSpeed, tgtSigRadius):
    """
    Calculate missile application factor.
    
    Formula: min(1, tgtSigRadius/eR, ((eV * tgtSigRadius) / (eR * tgtSpeed))^DRF)
    
    Args:
        atkEr: Missile explosion radius (aoeCloudSize) in meters
        atkEv: Missile explosion velocity (aoeVelocity) in m/s
        atkDrf: Missile damage reduction factor (aoeDamageReductionFactor)
        tgtSpeed: Target velocity (m/s)
        tgtSigRadius: Target signature radius (m)
    
    Returns:
        Application factor (0-1)
    """
    factors = [1]
    # "Slow" part - signature vs explosion radius
    if atkEr > 0:
        factors.append(tgtSigRadius / atkEr)
    # "Fast" part - explosion velocity vs target speed (raised to DRF power)
    if tgtSpeed > 0 and atkEr > 0:
        factors.append(((atkEv * tgtSigRadius) / (atkEr * tgtSpeed)) ** atkDrf)
    return min(factors)


# =============================================================================
# Multiplier Extraction
# =============================================================================

def _extractMultiplier(mod, attr):
    """
    Extract multiplier for a specific attribute.
    
    If the base value is 0 (e.g. Mjolnir has 0 thermal damage), we cannot
    calculate the multiplier by division (x / 0).
    
    In that case, we temporarily inject a base value of 1.0 into the modifier
    dictionary, read the modified value (which will be 1.0 * multiplier),
    and use that as the multiplier.
    """
    base = mod.getChargeBaseAttrValue(attr) or 0
    
    if base > 0:
        modified = mod.getModifiedChargeAttr(attr) or 0
        pyfalog.debug(f"DEBUG: _extractMultiplier({attr}): base={base}, modified={modified}, mult={modified/base}")
        return modified / base
    
    # Base is 0, we need to trick the eos logic to give us the multiplier
    # We use preAssign to set the base value to 1.0 for this calculation
    pyfalog.debug(f"DEBUG: _extractMultiplier({attr}): base is 0, attempting injection")
    mod.chargeModifiedAttributes.preAssign(attr, 1.0)
    try:
        # Get the modified value, which should now be 1.0 * multiplier
        multiplier = mod.getModifiedChargeAttr(attr) or 1.0
        pyfalog.debug(f"DEBUG: _extractMultiplier({attr}): injected base 1.0, got modified={multiplier}")
    finally:
        # Cleanup: remove the preAssign
        # Accessing private members is naughty but eos doesn't give us a clean way to remove preAssigns
        # and we must clean up to avoid side effects
        if attr in mod.chargeModifiedAttributes._ModifiedAttributeDict__preAssigns:
            del mod.chargeModifiedAttributes._ModifiedAttributeDict__preAssigns[attr]
            # Force recalculation by removing from cache
            if attr in mod.chargeModifiedAttributes._ModifiedAttributeDict__modified:
                del mod.chargeModifiedAttributes._ModifiedAttributeDict__modified[attr]
            if attr in mod.chargeModifiedAttributes._ModifiedAttributeDict__intermediary:
                del mod.chargeModifiedAttributes._ModifiedAttributeDict__intermediary[attr]
    
    return multiplier

def getDamageMultipliers(mod):
    """
    Extract per-damage-type multipliers by comparing modified to base values.
    
    This captures all skill bonuses (Warhead Upgrades, etc.) and ship bonuses
    that affect missile damage. Different damage types may have different bonuses
    (e.g., Gila has kinetic/thermal bonus).
    
    Args:
        mod: Launcher module with a charge loaded
    
    Returns:
        Dict with multipliers for emDamage, thermalDamage, kineticDamage, explosiveDamage
    """
    if mod.charge is None:
        return {
            'emDamage': 1.0,
            'thermalDamage': 1.0,
            'kineticDamage': 1.0,
            'explosiveDamage': 1.0
        }
    
    multipliers = {}
    for dmgType in ('emDamage', 'thermalDamage', 'kineticDamage', 'explosiveDamage'):
        multipliers[dmgType] = _extractMultiplier(mod, dmgType)
    
    return multipliers


def getFlightMultipliers(mod):
    """
    Extract flight attribute multipliers by comparing modified to base values.
    
    This captures skill bonuses from Missile Projection, Missile Bombardment,
    and ship bonuses that affect flight time/velocity.
    
    Args:
        mod: Launcher module with a charge loaded
    
    Returns:
        Dict with multipliers for maxVelocity and explosionDelay
    """
    if mod.charge is None:
        return {'maxVelocity': 1.0, 'explosionDelay': 1.0}
    
    multipliers = {}
    for attr in ('maxVelocity', 'explosionDelay'):
        multipliers[attr] = _extractMultiplier(mod, attr)
    
    return multipliers


def getApplicationMultipliers(mod):
    """
    Extract application attribute multipliers by comparing modified to base values.
    
    This captures skills like Guided Missile Precision, Target Navigation Prediction,
    and rigging/implant bonuses that affect explosion radius/velocity.
    
    Args:
        mod: Launcher module with a charge loaded
    
    Returns:
        Dict with multipliers for aoeCloudSize, aoeVelocity, aoeDamageReductionFactor
    """
    if mod.charge is None:
        return {'aoeCloudSize': 1.0, 'aoeVelocity': 1.0, 'aoeDamageReductionFactor': 1.0}
    
    multipliers = {}
    for attr in ('aoeCloudSize', 'aoeVelocity', 'aoeDamageReductionFactor'):
        multipliers[attr] = _extractMultiplier(mod, attr)
    
    return multipliers


def getAllMultipliers(mod):
    """
    Extract all multipliers (damage, flight, application) from a module.
    
    Args:
        mod: Launcher module with a charge loaded
    
    Returns:
        Tuple of (damageMults, flightMults, appMults)
    """
    # pyfalog.debug(f"DEBUG: getAllMultipliers called for {mod.item.name}, charge={mod.charge}")
    return (
        getDamageMultipliers(mod),
        getFlightMultipliers(mod),
        getApplicationMultipliers(mod)
    )


# =============================================================================
# Range Calculation
# =============================================================================

def calculateMissileRange(maxVelocity, mass, agility, flightTime):
    """
    Calculate missile range for a given flight time.
    
    Uses EVE formula accounting for acceleration time.
    Source: http://www.eveonline.com/ingameboard.asp?a=topic&threadID=1307419&page=1#15
    
    D_m = V_m * (T_m + T_0*[exp(- T_m/T_0)-1])
    
    Simplified: acceleration time = min(flightTime, mass * agility / 1e6)
    
    Args:
        maxVelocity: Missile max velocity (m/s)
        mass: Missile mass (kg)
        agility: Missile agility
        flightTime: Flight time (seconds)
    
    Returns:
        Range in meters
    """
    accelTime = min(flightTime, mass * agility / 1000000)
    # Average distance during acceleration (starts at 0, ends at maxVelocity)
    duringAcceleration = maxVelocity / 2 * accelTime
    # Distance at full speed
    fullSpeed = maxVelocity * (flightTime - accelTime)
    return duringAcceleration + fullSpeed


def getMissileRangeData(charge, shipRadius, damageMults=None, flightMults=None, appMults=None):
    """
    Calculate missile range data for a charge with applied multipliers.
    
    EVE missiles have discrete flight times - if flight time is 1.3s, there's
    a 30% chance of flying 2s and 70% chance of flying 1s.
    
    Args:
        charge: Missile charge item
        shipRadius: Launching ship's radius (affects flight time)
        damageMults: Damage multipliers dict (or None for base values)
        flightMults: Flight multipliers dict (or None for base values)
        appMults: Application multipliers dict (or None for base values)
    
    Returns:
        Dict with: lowerRange, higherRange, higherChance, maxEffectiveRange,
                   and all computed stats
    """
    if flightMults is None:
        flightMults = {'maxVelocity': 1.0, 'explosionDelay': 1.0}
    if appMults is None:
        appMults = {'aoeCloudSize': 1.0, 'aoeVelocity': 1.0, 'aoeDamageReductionFactor': 1.0}
    if damageMults is None:
        damageMults = {'emDamage': 1.0, 'thermalDamage': 1.0, 'kineticDamage': 1.0, 'explosiveDamage': 1.0}
    
    # Get base charge attributes
    baseVelocity = charge.getAttribute('maxVelocity') or 0
    baseExplosionDelay = charge.getAttribute('explosionDelay') or 0
    baseMass = charge.getAttribute('mass') or 1
    baseAgility = charge.getAttribute('agility') or 1
    
    if baseVelocity <= 0 or baseExplosionDelay <= 0:
        return None
    
    # Apply flight multipliers
    maxVelocity = baseVelocity * flightMults['maxVelocity']
    explosionDelay = baseExplosionDelay * flightMults['explosionDelay']
    
    # Calculate flight time (includes ship radius bonus)
    # Flight time has bonus based on ship radius: https://github.com/pyfa-org/Pyfa/issues/2083
    flightTime = explosionDelay / 1000 + shipRadius / maxVelocity
    
    # Discrete flight time: floor and ceil
    lowerTime = math.floor(flightTime)
    higherTime = math.ceil(flightTime)
    higherChance = flightTime - lowerTime  # Probability of flying the extra second
    
    # Calculate ranges
    lowerRange = calculateMissileRange(maxVelocity, baseMass, baseAgility, lowerTime)
    higherRange = calculateMissileRange(maxVelocity, baseMass, baseAgility, higherTime)
    
    # Make range center-to-surface (missiles spawn at ship center)
    lowerRange = max(0, lowerRange - shipRadius)
    higherRange = max(0, higherRange - shipRadius)
    
    # Max effective range uses ceil(flightTime) * velocity for sorting
    maxEffectiveRange = higherRange
    
    # Get application stats with multipliers
    baseEr = charge.getAttribute('aoeCloudSize') or 0
    baseEv = charge.getAttribute('aoeVelocity') or 0
    baseDrf = charge.getAttribute('aoeDamageReductionFactor') or 1
    
    explosionRadius = baseEr * appMults['aoeCloudSize']
    explosionVelocity = baseEv * appMults['aoeVelocity']
    damageReductionFactor = baseDrf * appMults['aoeDamageReductionFactor']
    
    # Get damage with multipliers
    baseEm = charge.getAttribute('emDamage') or 0
    baseThermal = charge.getAttribute('thermalDamage') or 0
    baseKinetic = charge.getAttribute('kineticDamage') or 0
    baseExplosive = charge.getAttribute('explosiveDamage') or 0
    
    em = baseEm * damageMults['emDamage']
    thermal = baseThermal * damageMults['thermalDamage']
    kinetic = baseKinetic * damageMults['kineticDamage']
    explosive = baseExplosive * damageMults['explosiveDamage']
    totalDamage = em + thermal + kinetic + explosive
    
    return {
        'lowerRange': lowerRange,
        'higherRange': higherRange,
        'higherChance': higherChance,
        'maxEffectiveRange': maxEffectiveRange,
        'explosionRadius': explosionRadius,
        'explosionVelocity': explosionVelocity,
        'damageReductionFactor': damageReductionFactor,
        'totalDamage': totalDamage,
        'emDamage': em,
        'thermalDamage': thermal,
        'kineticDamage': kinetic,
        'explosiveDamage': explosive
    }


# =============================================================================
# Charge Data Precomputation
# =============================================================================

# Damage type priority for tie-breaking (EM > Thermal > Kinetic > Explosive)
DAMAGE_TYPE_PRIORITY = {
    'em': 0,
    'thermal': 1,
    'kinetic': 2,
    'explosive': 3
}


def getDominantDamageType(chargeName):
    """
    Determine the dominant damage type of a missile based on its name.
    
    Mjolnir = EM, Inferno = Thermal, Scourge = Kinetic, Nova = Explosive
    
    Args:
        chargeName: Missile name
    
    Returns:
        'em', 'thermal', 'kinetic', 'explosive', or 'unknown'
    """
    nameLower = chargeName.lower()
    if 'mjolnir' in nameLower:
        return 'em'
    elif 'inferno' in nameLower:
        return 'thermal'
    elif 'scourge' in nameLower:
        return 'kinetic'
    elif 'nova' in nameLower:
        return 'explosive'
    return 'unknown'


def precomputeMissileChargeData(mod, charges, cycleTimeMs, shipRadius,
                                 damageMults=None, flightMults=None, appMults=None,
                                 tgtResists=None):
    """
    Pre-compute constant values for each missile charge.
    
    Args:
        mod: Launcher module
        charges: List of valid missile charges
        cycleTimeMs: Launcher cycle time in milliseconds
        shipRadius: Ship radius for flight calculations
        damageMults: Per-damage-type multipliers from skills/ship
        flightMults: Flight attribute multipliers
        appMults: Application attribute multipliers
        tgtResists: Target resist tuple (em, therm, kin, explo) or None
    
    Returns:
        List of charge data dicts, sorted by maxEffectiveRange descending
    """
    if damageMults is None:
        damageMults = {'emDamage': 1.0, 'thermalDamage': 1.0, 'kineticDamage': 1.0, 'explosiveDamage': 1.0}
    if flightMults is None:
        flightMults = {'maxVelocity': 1.0, 'explosionDelay': 1.0}
    if appMults is None:
        appMults = {'aoeCloudSize': 1.0, 'aoeVelocity': 1.0, 'aoeDamageReductionFactor': 1.0}
    
    # Get launcher damage multiplier
    launcherDamageMult = mod.getModifiedItemAttr('damageMultiplier') or 1
    
    chargeData = []
    for charge in charges:
        rangeData = getMissileRangeData(charge, shipRadius, damageMults, flightMults, appMults)
        if rangeData is None:
            continue
        
        # Apply target resists
        totalDamage = rangeData['totalDamage']
        if tgtResists:
            emRes, thermRes, kinRes, exploRes = tgtResists
            totalDamage = (
                rangeData['emDamage'] * (1 - emRes) +
                rangeData['thermalDamage'] * (1 - thermRes) +
                rangeData['kineticDamage'] * (1 - kinRes) +
                rangeData['explosiveDamage'] * (1 - exploRes)
            )
        
        # Calculate raw volley and DPS
        rawVolley = totalDamage * launcherDamageMult
        rawDps = rawVolley / (cycleTimeMs / 1000) if cycleTimeMs > 0 else 0
        
        # Get damage type priority for tie-breaking
        damageType = getDominantDamageType(charge.name)
        damagePriority = DAMAGE_TYPE_PRIORITY.get(damageType, 99)
        
        chargeData.append({
            'name': charge.name,
            'raw_volley': rawVolley,
            'raw_dps': rawDps,
            'lowerRange': rangeData['lowerRange'],
            'higherRange': rangeData['higherRange'],
            'higherChance': rangeData['higherChance'],
            'maxEffectiveRange': rangeData['maxEffectiveRange'],
            'explosionRadius': rangeData['explosionRadius'],
            'explosionVelocity': rangeData['explosionVelocity'],
            'damageReductionFactor': rangeData['damageReductionFactor'],
            'damage_priority': damagePriority
        })
    
    # Sort by maxEffectiveRange descending (longest range first for max range calculation)
    # Then by raw_dps descending for tie-breaking
    chargeData.sort(key=lambda x: (-x['maxEffectiveRange'], -x['raw_dps']))
    
    return chargeData


def getMaxEffectiveRange(chargeData):
    """
    Get the maximum effective range from precomputed charge data.
    
    Args:
        chargeData: List of precomputed charge data dicts
    
    Returns:
        Maximum effective range in meters
    """
    if not chargeData:
        return 0
    # Charge data is sorted by maxEffectiveRange descending
    return chargeData[0]['maxEffectiveRange']


# =============================================================================
# Applied Volley Calculation
# =============================================================================

def calculateRangeFactor(distance, lowerRange, higherRange, higherChance):
    """
    Calculate range factor for missile at a distance.
    
    Args:
        distance: Distance to target (m)
        lowerRange: Range at floor(flightTime)
        higherRange: Range at ceil(flightTime)
        higherChance: Probability of flying the extra second
    
    Returns:
        Range factor (0, higherChance, or 1)
    """
    if distance <= lowerRange:
        return 1.0
    elif distance <= higherRange:
        return higherChance
    else:
        return 0.0


def calculateAppliedVolley(chargeData, distance, tgtSpeed, tgtSigRadius):
    """
    Calculate applied volley for a missile charge at a distance.
    
    Args:
        chargeData: Single charge data dict
        distance: Distance to target (m)
        tgtSpeed: Target velocity (m/s) - can be modified by webs
        tgtSigRadius: Target signature radius (m) - can be modified by TPs
    
    Returns:
        Applied volley (damage accounting for range and application)
    """
    # Range factor (discrete: 1, higherChance, or 0)
    rangeFactor = calculateRangeFactor(
        distance,
        chargeData['lowerRange'],
        chargeData['higherRange'],
        chargeData['higherChance']
    )
    
    if rangeFactor == 0:
        return 0
    
    # Application factor
    appFactor = calcMissileFactor(
        chargeData['explosionRadius'],
        chargeData['explosionVelocity'],
        chargeData['damageReductionFactor'],
        tgtSpeed,
        tgtSigRadius
    )
    
    return chargeData['raw_volley'] * rangeFactor * appFactor


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

def findBestCharge(chargeData, distance, tgtSpeed, tgtSigRadius):
    """
    Find the best missile charge at a distance.
    
    Uses damage type priority (EM > Thermal > Kinetic > Explosive) as tie-breaker.
    
    Args:
        chargeData: List of charge data dicts
        distance: Distance to target (m)
        tgtSpeed: Target velocity (m/s)
        tgtSigRadius: Target signature radius (m)
    
    Returns:
        Tuple of (best_volley, best_name, best_index)
    """
    bestVolley = 0
    bestName = None
    bestIndex = 0
    bestPriority = 99
    
    for i, cd in enumerate(chargeData):
        volley = calculateAppliedVolley(cd, distance, tgtSpeed, tgtSigRadius)
        
        # Tie-break: higher volley wins; if equal, lower damage_priority wins
        if volley > bestVolley or (volley == bestVolley and volley > 0 and cd['damage_priority'] < bestPriority):
            bestVolley = volley
            bestName = cd['name']
            bestIndex = i
            bestPriority = cd['damage_priority']
    
    return bestVolley, bestName, bestIndex


# =============================================================================
# Transition Point Calculation
# =============================================================================

def _updateParamsWithCache(baseTgtSpeed, baseTgtSigRadius, projectedCache, distance):
    """
    Update target params using projected cache for webs/TPs.
    
    Args:
        baseTgtSpeed: Base target speed (from graph params)
        baseTgtSigRadius: Base target sig radius
        projectedCache: Pre-built cache from buildProjectedCache()
        distance: Distance in meters
    
    Returns:
        Tuple of (tgtSpeed, tgtSigRadius) with projected effects applied
    """
    projected = getProjectedParamsAtDistance(projectedCache, distance)
    return projected['tgtSpeed'], projected['tgtSigRadius']


def calculateTransitions(chargeData, baseTgtSpeed, baseTgtSigRadius,
                         projectedCache, maxDistance=300000, resolution=100):
    """
    Calculate distances where optimal missile ammo changes.
    
    Args:
        chargeData: List of charge data dicts
        baseTgtSpeed: Base target speed (from graph params)
        baseTgtSigRadius: Base target sig radius
        projectedCache: Pre-built cache for webs/TPs
        maxDistance: Maximum distance to scan (m)
    
    Returns:
        List of tuples: [(distance, charge_index, charge_name, volley), ...]
    """
    if not chargeData:
        return []
    
    pyfalog.debug(f"[MISSILE] Starting transition calculation with {len(chargeData)} charges")
    pyfalog.debug(f"[MISSILE] Base params: tgtSpeed={baseTgtSpeed}, tgtSig={baseTgtSigRadius}")
    
    transitions = []
    currentCharge = None
    
    # Start at distance 0
    tgtSpeed, tgtSigRadius = _updateParamsWithCache(baseTgtSpeed, baseTgtSigRadius, projectedCache, 0)
    bestVolley, bestName, bestIdx = findBestCharge(chargeData, 0, tgtSpeed, tgtSigRadius)
    transitions.append((0, bestIdx, bestName, bestVolley))
    currentCharge = bestName
    
    # Scan for transitions
    distance = resolution
    while distance <= maxDistance:
        tgtSpeed, tgtSigRadius = _updateParamsWithCache(baseTgtSpeed, baseTgtSigRadius, projectedCache, distance)
        bestVolley, bestName, bestIdx = findBestCharge(chargeData, distance, tgtSpeed, tgtSigRadius)
        
        if bestName != currentCharge:
            # Binary search for exact transition point
            low, high = distance - resolution, distance
            while high - low > 10:
                mid = (low + high) // 2
                midSpeed, midSig = _updateParamsWithCache(baseTgtSpeed, baseTgtSigRadius, projectedCache, mid)
                _, midName, _ = findBestCharge(chargeData, mid, midSpeed, midSig)
                if midName == currentCharge:
                    low = mid
                else:
                    high = mid
            
            # Get volley at transition
            highSpeed, highSig = _updateParamsWithCache(baseTgtSpeed, baseTgtSigRadius, projectedCache, high)
            bestVolley, _, _ = findBestCharge(chargeData, high, highSpeed, highSig)
            
            transitions.append((high, bestIdx, bestName, bestVolley))
            pyfalog.debug(f"[MISSILE] Transition @ {high/1000:.1f}km: {currentCharge} -> {bestName}")
            currentCharge = bestName
        
        # Stop if we're past all missile ranges
        if bestVolley < 0.01:
            transitions.append((distance, -1, None, 0))
            break
        
        distance += resolution
    
    pyfalog.debug(f"[MISSILE] Completed: {len(transitions)} transition points found")
    
    return transitions


# =============================================================================
# Query Functions
# =============================================================================

def getVolleyAtDistance(transitions, chargeData, distance,
                        baseTgtSpeed, baseTgtSigRadius, projectedCache):
    """
    Get applied volley at a specific distance.
    
    Args:
        transitions: List of transition tuples
        chargeData: List of charge data dicts
        distance: Distance to query (m)
        baseTgtSpeed: Base target speed
        baseTgtSigRadius: Base target sig radius
        projectedCache: Pre-built projected cache
    
    Returns:
        Tuple of (volley, charge_name)
    """
    if not transitions or not chargeData:
        return 0, None
    
    # Find which charge is optimal at this distance
    distances = [t[0] for t in transitions]
    idx = bisect_right(distances, distance) - 1
    if idx < 0:
        idx = 0
    
    chargeIdx = transitions[idx][1]
    if chargeIdx < 0 or chargeIdx >= len(chargeData):
        return 0, None
    
    cd = chargeData[chargeIdx]
    
    # Calculate exact volley with projected effects
    tgtSpeed, tgtSigRadius = _updateParamsWithCache(baseTgtSpeed, baseTgtSigRadius, projectedCache, distance)
    volley = calculateAppliedVolley(cd, distance, tgtSpeed, tgtSigRadius)
    
    return volley, cd['name']

