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

from logbook import Logger

from eos.const import FittingHardpoint
from graphs.data.base import FitGraph, XDef, YDef, Input, VectorDef
from graphs.data.fitDamageProjection.getter import (
    Distance2OptimalAmmoDpsGetter,
    Distance2OptimalAmmoVolleyGetter,
)
from graphs.data.fitDamageProjection.calc.turret import getTurretBaseStats
from graphs.data.fitDamageProjection.calc.charges import getChargeStats
from graphs.data.fitDamageProjection.calc.valid_charges import getValidChargesForModule
from graphs.data.fitDamageProjection.calc.launcher import getFlightMultipliers
from graphs.data.fitDamageStats.cache import ProjectedDataCache
from service.const import GraphCacheCleanupReason
from service.settings import GraphSettings

pyfalog = Logger(__name__)


class FitDamageProjectionGraph(FitGraph):

    # Graph definition
    internalName = 'dmgEnvelopeGraph'
    name = 'Damage Projection'
    xDefs = [
        XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km'))]
    inputs = [
        Input(handle='distance', unit='km', label='Distance', iconID=None, defaultValue=None, defaultRange=(0, 100), mainTooltip='Distance to target')]
    
    srcVectorDef = VectorDef(lengthHandle='atkSpeed', lengthUnit='%', angleHandle='atkAngle', angleUnit='degrees', label='Attacker')
    tgtVectorDef = VectorDef(lengthHandle='tgtSpeed', lengthUnit='%', angleHandle='tgtAngle', angleUnit='degrees', label='Target')

    hasTargets = True
    srcExtraCols = ('Dps', 'Volley', 'Speed', 'SigRadius', 'Radius')
    
    @property
    def tgtExtraCols(self):
        """Define target extra columns similar to Damage Stats graph"""
        cols = ['Target Resists', 'Speed', 'SigRadius', 'Radius']
        return cols

    @property
    def yDefs(self):
        ignoreResists = GraphSettings.getInstance().get('ignoreResists')
        return [
            YDef(handle='dps', unit=None, label='DPS' if ignoreResists else 'Effective DPS'),
            YDef(handle='volley', unit=None, label='Volley' if ignoreResists else 'Effective Volley')]

    # Normalizers convert input values to internal units
    _normalizers = {
        ('distance', 'km'): lambda v, src, tgt: None if v is None else v * 1000,
        ('atkSpeed', '%'): lambda v, src, tgt: v / 100 * src.getMaxVelocity(),
        ('tgtSpeed', '%'): lambda v, src, tgt: v / 100 * tgt.getMaxVelocity()}
    
    # Denormalizers convert internal units back to display units
    _denormalizers = {
        ('distance', 'km'): lambda v, src, tgt: None if v is None else v / 1000,
        ('tgtSpeed', '%'): lambda v, src, tgt: v * 100 / tgt.getMaxVelocity()}
    
    # No limiters - allow user to specify any range they want
    _limiters = {}

    _getters = {
        ('distance', 'dps'): Distance2OptimalAmmoDpsGetter,
        ('distance', 'volley'): Distance2OptimalAmmoVolleyGetter}

    def __init__(self):
        super().__init__()
        self._projectedCache = ProjectedDataCache()
        self._rangeCache = {}

    def getDefaultInputRange(self, inputDef, sources):
        """
        Calculate dynamic default range based on the turrets/missiles max effective range.
        
        Returns (min, max) tuple in the input's units (km for distance).
        For turrets: the longest range ammo's optimal+falloff*2 + 10%, capped at 300km.
        For missiles: the longest range missile's max range + 10%, capped at 300km.
        """
        if inputDef.handle != 'distance' or not sources:
            return inputDef.defaultRange
        
        # Build cache key from fit IDs
        fitIDs = frozenset(src.item.ID for src in sources if src.item is not None)
        if not fitIDs:
            return inputDef.defaultRange
        
        # Check cache
        if fitIDs in self._rangeCache:
            return self._rangeCache[fitIDs]
        
        max_range_m = 0
        
        for src in sources:
            fit = src.item
            if fit is None:
                continue
            
            # Check all turrets and missiles
            for mod in fit.activeModulesIter():
                if mod.hardpoint == FittingHardpoint.TURRET:
                    if mod.getModifiedItemAttr('miningAmount'):
                        continue
                    
                    # Get turret base stats
                    turret_base = getTurretBaseStats(mod)
                    
                    # Check all compatible charges for this turret
                    for charge in getValidChargesForModule(mod):
                        charge_stats = getChargeStats(charge)
                        
                        # Calculate effective optimal + 2*falloff (where DPS drops to ~6%)
                        effective_optimal = turret_base['optimal'] * charge_stats['rangeMultiplier']
                        effective_falloff = turret_base['falloff'] * charge_stats['falloffMultiplier']
                        effective_max = effective_optimal + effective_falloff * 2.5
                        
                        if effective_max > max_range_m:
                            max_range_m = effective_max
                
                elif mod.hardpoint == FittingHardpoint.MISSILE:
                    # For missiles, check ALL compatible charges to find longest range
                    # We need the max range across all ammo types, not just the loaded one
                    
                    valid_charges = list(getValidChargesForModule(mod))
                    if not valid_charges:
                        continue

                    # Get flight multipliers from skills/ship (handling empty launcher case)
                    if mod.charge is None:
                        # Temp load first valid charge to extract multipliers
                        temp_charge = valid_charges[0]
                        mod.charge = temp_charge
                        if mod.owner:
                            mod.owner.calculated = False
                            mod.owner.calculateModifiedAttributes()
                        
                        flight_mults = getFlightMultipliers(mod)
                        
                        # Cleanup
                        mod.charge = None
                        if mod.owner:
                            mod.owner.calculated = False
                            mod.owner.calculateModifiedAttributes()
                    else:
                        flight_mults = getFlightMultipliers(mod)
                    
                    for charge in valid_charges:
                        base_velocity = charge.getAttribute('maxVelocity') or 0
                        base_explosion_delay = charge.getAttribute('explosionDelay') or 0
                        if base_velocity > 0 and base_explosion_delay > 0:
                            # Apply skill/ship bonuses to flight attributes
                            maxVelocity = base_velocity * flight_mults['maxVelocity']
                            explosionDelay = base_explosion_delay * flight_mults['explosionDelay']
                            # Estimate range: velocity * flight_time
                            flightTime = explosionDelay / 1000
                            estimated_range = maxVelocity * flightTime * 1.1
                            if estimated_range > max_range_m:
                                max_range_m = estimated_range
        
        if max_range_m <= 0:
            return inputDef.defaultRange
        
        # Add 10% buffer and convert to km
        max_range_km = (max_range_m * 1.1) / 1000
        
        # Cap at 300km (EVE's max lock range)
        max_range_km = min(max_range_km, 300)
        
        # Round to nice number
        max_range_km = int(max_range_km + 0.5)
        
        result = (0, max_range_km)
        self._rangeCache[fitIDs] = result
        return result

    def _clearInternalCache(self, reason, extraData):
        pyfalog.debug(f"[CLEAR-CACHE] _clearInternalCache called: reason={reason}, extraData={extraData}")

        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            # extraData is the fit ID (integer), not the fit object
            fit_id = extraData
            pyfalog.debug(f"[CLEAR-CACHE] Clearing caches for fit ID {fit_id}")

            # Clear base projected cache for this fit
            self._projectedCache.clearForFit(fit_id)

            # Clear weapon cache entries for this specific fit only
            # Cache key format: (fitID, weaponType, qualityTier, tgtResists, applyProjected, tgtSpeed, tgtSigRadius)
            if hasattr(self, '_ammo_weapon_cache'):
                keys_to_remove = [k for k in self._ammo_weapon_cache.keys() if k[0] == fit_id]
                for key in keys_to_remove:
                    del self._ammo_weapon_cache[key]
                pyfalog.debug(f"[CLEAR-CACHE] Removed {len(keys_to_remove)} weapon cache entries for fit {fit_id}")

            # Clear projected cache entries for this specific fit (all target combinations)
            # Projected cache key format: (fitID, tgtSpeed, tgtSigRadius)
            if hasattr(self, '_ammo_projected_cache'):
                keys_to_remove = [k for k in self._ammo_projected_cache.keys() if k[0] == fit_id]
                for key in keys_to_remove:
                    del self._ammo_projected_cache[key]
                pyfalog.debug(f"[CLEAR-CACHE] Removed {len(keys_to_remove)} projected cache entries for fit {fit_id}")

            # Clear range cache entries that include this fit ID
            if hasattr(self, '_rangeCache'):
                keys_to_remove = [k for k in self._rangeCache.keys() if fit_id in k]
                for key in keys_to_remove:
                    del self._rangeCache[key]
                pyfalog.debug(f"[CLEAR-CACHE] Removed {len(keys_to_remove)} range cache entries for fit {fit_id}")
            
            # Clear charge cache - when fits change, weapon types might change
            if hasattr(self, '_ammo_charge_cache'):
                count = len(self._ammo_charge_cache)
                self._ammo_charge_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} charge cache entries for fit change")

        elif reason in (GraphCacheCleanupReason.profileChanged, GraphCacheCleanupReason.profileRemoved):
            profile_id = extraData
            pyfalog.debug(f"[CLEAR-CACHE] Clearing caches for profile ID {profile_id}")

            if hasattr(self, '_ammo_weapon_cache'):
                count = len(self._ammo_weapon_cache)
                self._ammo_weapon_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} weapon cache entries due to profile change")

            if hasattr(self, '_ammo_projected_cache'):
                count = len(self._ammo_projected_cache)
                self._ammo_projected_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} projected cache entries due to profile change")
            
            if hasattr(self, '_rangeCache'):
                count = len(self._rangeCache)
                self._rangeCache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} range cache entries due to profile change")

        elif reason == GraphCacheCleanupReason.graphSwitched:
            self._projectedCache.clearAll()
            pyfalog.debug(f"[CLEAR-CACHE] Clearing ALL caches for graph switch")

            # Clear all ammo caches globally
            if hasattr(self, '_ammo_weapon_cache'):
                count = len(self._ammo_weapon_cache)
                self._ammo_weapon_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} weapon cache entries")

            if hasattr(self, '_ammo_projected_cache'):
                count = len(self._ammo_projected_cache)
                self._ammo_projected_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} projected cache entries")
            
            if hasattr(self, '_rangeCache'):
                count = len(self._rangeCache)
                self._rangeCache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} range cache entries")

            if hasattr(self, '_ammo_charge_cache'):
                count = len(self._ammo_charge_cache)
                self._ammo_charge_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} charge cache entries")

        elif reason in (GraphCacheCleanupReason.inputChanged, GraphCacheCleanupReason.optionChanged):
            pyfalog.debug(f"[CLEAR-CACHE] Clearing ALL caches for {reason.name}")
            
            if hasattr(self, '_ammo_weapon_cache'):
                count = len(self._ammo_weapon_cache)
                self._ammo_weapon_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} weapon cache entries due to {reason.name}")

            if hasattr(self, '_ammo_projected_cache'):
                count = len(self._ammo_projected_cache)
                self._ammo_projected_cache = {}
                pyfalog.debug(f"[CLEAR-CACHE] Cleared {count} projected cache entries due to {reason.name}")


    def getPlotSegments(self, mainInput, miscInputs, xSpec, ySpec, src, tgt=None):
        """
        Get segmented plot data with ammo information for color coding.
        
        Returns list of segments, each with xs, ys, ammo name, and ammo index.
        Returns None if this graph doesn't support segments or getter doesn't have getSegments.
        """
        pyfalog.debug(f"[GRAPH] getPlotSegments called for src={src.item.name}, mainInput.value={mainInput.value}")
        try:
            getterClass = self._getters[(xSpec.handle, ySpec.handle)]
        except KeyError:
            pyfalog.debug(f"[GRAPH] No getter for ({xSpec.handle}, {ySpec.handle})")
            return None
        
        # Normalize the input range
        mainParamRange = self._normalizeMain(mainInput=mainInput, src=src, tgt=tgt)
        miscParams = self._normalizeMisc(miscInputs=miscInputs, src=src, tgt=tgt)
        mainParamRange = self._limitMain(mainParamRange=mainParamRange, src=src, tgt=tgt)
        miscParams = self._limitMisc(miscParams=miscParams, src=src, tgt=tgt)
        pyfalog.debug(f"[GRAPH] Normalized mainParamRange={mainParamRange}")
        
        getter = getterClass(graph=self)
        
        # Check if getter has getSegments method
        if not hasattr(getter, 'getSegments'):
            pyfalog.debug(f"[GRAPH] Getter has no getSegments method")
            return None
        
        segments = getter.getSegments(
            xRange=mainParamRange[1], 
            miscParams=miscParams, 
            src=src, 
            tgt=tgt)
        
        pyfalog.debug(f"[GRAPH] getter.getSegments returned {len(segments) if segments else segments} segments")
        
        if not segments:
            pyfalog.debug(f"[GRAPH] No segments, returning None")
            return None
        
        # Denormalize the values back to display units
        for segment in segments:
            segment['xs'] = self._denormalizeValues(values=segment['xs'], axisSpec=xSpec, src=src, tgt=tgt)
            segment['ys'] = self._denormalizeValues(values=segment['ys'], axisSpec=ySpec, src=src, tgt=tgt)
        
        pyfalog.debug(f"[GRAPH] Returning {len(segments)} denormalized segments for {src.item.name}")
        return segments

    def getPointExtended(self, x, miscInputs, xSpec, ySpec, src, tgt=None):
        """
        Get point value with extended info (like ammo name) at x.
        
        Returns (y_value, extra_info_dict) tuple.
        extra_info_dict may contain 'ammo' key with the ammo name.
        """
        try:
            getterClass = self._getters[(xSpec.handle, ySpec.handle)]
        except KeyError:
            return None, {}
        
        x = self._normalizeValue(value=x, axisSpec=xSpec, src=src, tgt=tgt)
        miscParams = self._normalizeMisc(miscInputs=miscInputs, src=src, tgt=tgt)
        miscParams = self._limitMisc(miscParams=miscParams, src=src, tgt=tgt)
        
        getter = getterClass(graph=self)
        
        # Check if getter has getPointExtended method
        if hasattr(getter, 'getPointExtended'):
            y, extraInfo = getter.getPointExtended(x=x, miscParams=miscParams, src=src, tgt=tgt)
            y = self._denormalizeValue(value=y, axisSpec=ySpec, src=src, tgt=tgt)
            return y, extraInfo
        else:
            # Fall back to regular getPoint
            y = self._getPoint(x=x, miscParams=miscParams, xSpec=xSpec, ySpec=ySpec, src=src, tgt=tgt)
            y = self._denormalizeValue(value=y, axisSpec=ySpec, src=src, tgt=tgt)
            return y, {}

    def _updateMiscParams(self, **kwargs):
        miscParams = super()._updateMiscParams(**kwargs)
        # Set defaults from target profile
        miscParams['tgtSigRadius'] = miscParams['tgt'].getSigRadius()
        miscParams['tgtSpeed'] = miscParams['tgt'].getMaxVelocity()
        miscParams.setdefault('atkSpeed', 0)
        miscParams.setdefault('atkAngle', 0)
        miscParams.setdefault('tgtAngle', 0)
        return miscParams
