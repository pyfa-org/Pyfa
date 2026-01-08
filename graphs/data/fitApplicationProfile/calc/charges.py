# =============================================================================
# Constants
# =============================================================================

# Navy faction ammo prefixes (for S/M/L ammo)
NAVY_PREFIXES = (
    'Imperial Navy ',
    'Republic Fleet ', 
    'Caldari Navy ',
    'Federation Navy '
)

# Capital (XL) "navy-tier" faction ammo prefixes
# There is no empire Navy XL ammo, so pirate faction serves as the "navy" tier for capitals
CAPITAL_NAVY_PREFIXES = (
    'Sansha ',
    'Arch Angel ',
    'Shadow '
)


# =============================================================================
# Quality Tier Filtering
# =============================================================================

def filterChargesByQuality(charges, qualityTier):
    """
    Filter charges based on quality tier selection.
    
    Args:
        charges: List of charge items
        qualityTier: 't1', 'navy', or 'all'
    
    Returns:
        Filtered list of charges
        
    Tiers are cumulative:
        - 't1': Tech I (metaGroup 1) + Tech II (metaGroup 2)
        - 'navy': t1 + Navy faction ammo (Imperial Navy, Republic Fleet, Caldari Navy, Federation Navy)
                  For XL (capital) ammo: includes pirate faction (Sansha, Arch Angel, Shadow)
        - 'all': Everything including high-tier faction (Blood, Dark Blood, True Sansha, etc.)
    
    Tech II ammo is always included as it's a distinct ammo type, not a "better" variant.
    """
    if qualityTier == 'all':
        return charges
    
    filtered = []
    for charge in charges:
        mg = charge.metaGroup
        mgId = mg.ID if mg else None
        
        # Tech I (metaGroup 1) - always included
        if mgId == 1:
            filtered.append(charge)
            continue
        
        # Tech II (metaGroup 2) - always included (distinct ammo type like Conflagration, Void, etc.)
        if mgId == 2:
            filtered.append(charge)
            continue
        
        # For 'navy' tier, include Navy faction ammo
        if qualityTier == 'navy' and mgId == 4:  # Faction
            # Check if it's XL (capital) ammo by name suffix
            isCapital = charge.name.endswith(' XL')
            
            if isCapital:
                # For capital ammo, use pirate faction prefixes as "navy" tier
                if any(charge.name.startswith(prefix) for prefix in CAPITAL_NAVY_PREFIXES):
                    filtered.append(charge)
            else:
                # For subcap ammo, use empire Navy prefixes
                if any(charge.name.startswith(prefix) for prefix in NAVY_PREFIXES):
                    filtered.append(charge)
    
    return filtered if filtered else charges


# =============================================================================
# Charge Stats Extraction
# =============================================================================

def getChargeStats(charge):
    """
    Extract charge stats including damage values and multipliers.
    
    Args:
        charge: The charge item
    
    Returns:
        Dict with damage values and range/falloff/tracking multipliers
    """
    em = charge.getAttribute('emDamage') or 0
    thermal = charge.getAttribute('thermalDamage') or 0
    kinetic = charge.getAttribute('kineticDamage') or 0
    explosive = charge.getAttribute('explosiveDamage') or 0
    
    return {
        'emDamage': em,
        'thermalDamage': thermal,
        'kineticDamage': kinetic,
        'explosiveDamage': explosive,
        'totalDamage': em + thermal + kinetic + explosive,
        'rangeMultiplier': charge.getAttribute('weaponRangeMultiplier') or 1,
        'falloffMultiplier': charge.getAttribute('fallofMultiplier') or 1,  # EVE typo
        'trackingMultiplier': charge.getAttribute('trackingSpeedMultiplier') or 1
    }


# =============================================================================
# Resist Application
# =============================================================================

def applyResists(chargeStats, tgtResists):
    """
    Apply target resists to charge stats.
    
    Args:
        chargeStats: Dict from getChargeStats
        tgtResists: Tuple of (em, therm, kin, explo) resist values (0-1)
    
    Returns:
        New dict with resisted damage values
    """
    if not tgtResists:
        return chargeStats
    
    emRes, thermRes, kinRes, exploRes = tgtResists
    
    em = chargeStats['emDamage'] * (1 - emRes)
    thermal = chargeStats['thermalDamage'] * (1 - thermRes)
    kinetic = chargeStats['kineticDamage'] * (1 - kinRes)
    explosive = chargeStats['explosiveDamage'] * (1 - exploRes)
    
    result = chargeStats.copy()
    result.update({
        'emDamage': em,
        'thermalDamage': thermal,
        'kineticDamage': kinetic,
        'explosiveDamage': explosive,
        'totalDamage': em + thermal + kinetic + explosive
    })
    return result


# =============================================================================
# Charge Data Precomputation
# =============================================================================

def precomputeChargeData(turretBase, charges, skillMult=1.0, tgtResists=None):
    """
    Pre-compute constant values for each charge.
    
    This computes effective stats (turret base * charge multipliers) and
    raw volley for each charge, which can then be used for fast lookups.
    
    Args:
        turretBase: Base turret stats dict from getTurretBaseStats
        charges: List of charge items
        skillMult: Skill damage multiplier from getSkillMultiplier
        tgtResists: Target resists tuple or None
    
    Returns:
        List of dicts with: name, raw_volley, effective_optimal, 
        effective_falloff, effective_tracking
    
    Note: We do NOT store raw_dps - it's derived from raw_volley / cycle_time
    when needed at the mixin level.
    """
    chargeData = []
    
    for charge in charges:
        stats = getChargeStats(charge)
        
        # Apply resists early for efficiency
        if tgtResists:
            stats = applyResists(stats, tgtResists)
        
        # Compute effective turret stats with charge modifiers
        effectiveOptimal = turretBase['optimal'] * stats['rangeMultiplier']
        effectiveFalloff = turretBase['falloff'] * stats['falloffMultiplier']
        effectiveTracking = turretBase['tracking'] * stats['trackingMultiplier']
        
        # Compute raw volley (unmodified by range/tracking)
        rawVolley = stats['totalDamage'] * skillMult * turretBase['damageMultiplier']
        
        chargeData.append({
            'name': charge.name,
            'raw_volley': rawVolley,
            'effective_optimal': effectiveOptimal,
            'effective_falloff': effectiveFalloff,
            'effective_tracking': effectiveTracking
        })
    
    return chargeData


def getLongestRangeMultiplier(charges):
    """
    Get the maximum range multiplier from a list of charges.
    
    Used to calculate the max effective range of a turret for cache sizing.
    
    Args:
        charges: List of charge items
    
    Returns:
        The highest rangeMultiplier value among all charges
    """
    if not charges:
        return 1.0
    
    maxRangeMult = 1.0
    for charge in charges:
        rangeMult = charge.getAttribute('weaponRangeMultiplier') or 1.0
        if rangeMult > maxRangeMult:
            maxRangeMult = rangeMult
    
    return maxRangeMult
