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


import eos.config
from eos.const import FittingHardpoint
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from eos.utils.stats import DmgTypes
from gui.builtinGraphs.base import FitGraph, XDef, YDef, Input, VectorDef
from service.const import GraphCacheCleanupReason
from .calc import getTurretMult, getLauncherMult, getDroneMult, getFighterAbilityMult, getSmartbombMult, getBombMult, getGuidedBombMult
from .timeCache import TimeCache


class FitDamageStatsGraph(FitGraph):

    def __init__(self):
        super().__init__()
        self._timeCache = TimeCache()

    def _clearInternalCache(self, reason, extraData):
        # Here, we care only about fit changes and graph changes.
        # - Input changes are irrelevant as time cache cares only about
        # time input, and it regenerates once time goes beyond cached value
        # - Option changes are irrelevant as cache contains "raw" damage
        # values which do not rely on any graph options
        if reason == GraphCacheCleanupReason.fitChanged:
            self._timeCache.clearForFit(extraData)
        elif reason == GraphCacheCleanupReason.graphSwitched:
            self._timeCache.clearAll()

    # UI stuff
    internalName = 'dmgStatsGraph'
    name = 'Damage Stats'
    xDefs = [
        XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km')),
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
        XDef(handle='tgtSpeed', unit='m/s', label='Target speed', mainInput=('tgtSpeed', '%')),
        XDef(handle='tgtSpeed', unit='%', label='Target speed', mainInput=('tgtSpeed', '%')),
        XDef(handle='tgtSigRad', unit='m', label='Target signature radius', mainInput=('tgtSigRad', '%')),
        XDef(handle='tgtSigRad', unit='%', label='Target signature radius', mainInput=('tgtSigRad', '%'))]
    yDefs = [
        YDef(handle='dps', unit=None, label='DPS'),
        YDef(handle='volley', unit=None, label='Volley'),
        YDef(handle='damage', unit=None, label='Damage inflicted')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=None, defaultRange=(0, 80), mainOnly=False),
        Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=50, defaultRange=(0, 100), mainOnly=False),
        Input(handle='tgtSpeed', unit='%', label='Target speed', iconID=1389, defaultValue=100, defaultRange=(0, 100), mainOnly=False),
        Input(handle='tgtSigRad', unit='%', label='Target signature', iconID=1390, defaultValue=100, defaultRange=(100, 200), mainOnly=True)]
    srcVectorDef = VectorDef(lengthHandle='atkSpeed', lengthUnit='%', angleHandle='atkAngle', angleUnit='degrees', label='Attacker')
    tgtVectorDef = VectorDef(lengthHandle='tgtSpeed', lengthUnit='%', angleHandle='tgtAngle', angleUnit='degrees', label='Target')
    hasTargets = True

    # Calculation stuff
    _normalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v * 1000,
        ('atkSpeed', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('maxVelocity'),
        ('tgtSpeed', '%'): lambda v, fit, tgt: v / 100 * tgt.ship.getModifiedItemAttr('maxVelocity'),
        ('tgtSigRad', '%'): lambda v, fit, tgt: v / 100 * tgt.ship.getModifiedItemAttr('signatureRadius')}
    _limiters = {
        'time': lambda fit, tgt: (0, 2500)}
    _denormalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v / 1000,
        ('tgtSpeed', '%'): lambda v, fit, tgt: v * 100 / tgt.ship.getModifiedItemAttr('maxVelocity'),
        ('tgtSigRad', '%'): lambda v, fit, tgt: v * 100 / tgt.ship.getModifiedItemAttr('signatureRadius')}

    def _distance2dps(self, mainInput, miscInputs, fit, tgt):
        return self._xDistanceGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getDpsPerKey, timeCachePrepFunc=self._timeCache.prepareDpsData)

    def _distance2volley(self, mainInput, miscInputs, fit, tgt):
        return self._xDistanceGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getVolleyPerKey, timeCachePrepFunc=self._timeCache.prepareVolleyData)

    def _distance2damage(self, mainInput, miscInputs, fit, tgt):
        return self._xDistanceGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getDmgPerKey, timeCachePrepFunc=self._timeCache.prepareDmgData)

    def _time2dps(self, mainInput, miscInputs, fit, tgt):
        return self._xTimeGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            timeCachePrepFunc=self._timeCache.prepareDpsData, timeCacheGetFunc=self._timeCache.getDpsData)

    def _time2volley(self, mainInput, miscInputs, fit, tgt):
        return self._xTimeGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            timeCachePrepFunc=self._timeCache.prepareVolleyData, timeCacheGetFunc=self._timeCache.getVolleyData)

    def _time2damage(self, mainInput, miscInputs, fit, tgt):
        return self._xTimeGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            timeCachePrepFunc=self._timeCache.prepareDmgData, timeCacheGetFunc=self._timeCache.getDmgData)

    def _tgtSpeed2dps(self, mainInput, miscInputs, fit, tgt):
        return self._xTgtSpeedGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getDpsPerKey, timeCachePrepFunc=self._timeCache.prepareDpsData)

    def _tgtSpeed2volley(self, mainInput, miscInputs, fit, tgt):
        return self._xTgtSpeedGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getVolleyPerKey, timeCachePrepFunc=self._timeCache.prepareVolleyData)

    def _tgtSpeed2damage(self, mainInput, miscInputs, fit, tgt):
        return self._xTgtSpeedGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getDmgPerKey, timeCachePrepFunc=self._timeCache.prepareDmgData)

    def _tgtSigRad2dps(self, mainInput, miscInputs, fit, tgt):
        return self._xTgtSigRadiusGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getDpsPerKey, timeCachePrepFunc=self._timeCache.prepareDpsData)

    def _tgtSigRad2volley(self, mainInput, miscInputs, fit, tgt):
        return self._xTgtSigRadiusGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getVolleyPerKey, timeCachePrepFunc=self._timeCache.prepareVolleyData)

    def _tgtSigRad2damage(self, mainInput, miscInputs, fit, tgt):
        return self._xTgtSigRadiusGetter(
            mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt,
            dmgFunc=self._getDmgPerKey, timeCachePrepFunc=self._timeCache.prepareDmgData)

    _getters = {
        ('distance', 'dps'): _distance2dps,
        ('distance', 'volley'): _distance2volley,
        ('distance', 'damage'): _distance2damage,
        ('time', 'dps'): _time2dps,
        ('time', 'volley'): _time2volley,
        ('time', 'damage'): _time2damage,
        ('tgtSpeed', 'dps'): _tgtSpeed2dps,
        ('tgtSpeed', 'volley'): _tgtSpeed2volley,
        ('tgtSpeed', 'damage'): _tgtSpeed2damage,
        ('tgtSigRad', 'dps'): _tgtSigRad2dps,
        ('tgtSigRad', 'volley'): _tgtSigRad2volley,
        ('tgtSigRad', 'damage'): _tgtSigRad2damage}

    # Point getter helpers
    def _xDistanceGetter(self, mainInput, miscInputs, fit, tgt, dmgFunc, timeCachePrepFunc):
        xs = []
        ys = []
        tgtSigRadius = tgt.ship.getModifiedItemAttr('signatureRadius')
        # Process inputs into more convenient form
        miscInputMap = dict(miscInputs)
        # Get all data we need for all distances into maps/caches
        timeCachePrepFunc(fit, miscInputMap['time'])
        dmgMap = dmgFunc(fit=fit, time=miscInputMap['time'])
        # Go through distances and calculate distance-dependent data
        for distance in self._iterLinear(mainInput[1]):
            applicationMap = self._getApplicationPerKey(
                fit=fit,
                tgt=tgt,
                atkSpeed=miscInputMap['atkSpeed'],
                atkAngle=miscInputMap['atkAngle'],
                distance=distance,
                tgtSpeed=miscInputMap['tgtSpeed'],
                tgtAngle=miscInputMap['tgtAngle'],
                tgtSigRadius=tgtSigRadius)
            dmg = self._aggregate(dmgMap=dmgMap, applicationMap=applicationMap).total
            xs.append(distance)
            ys.append(dmg)
        return xs, ys

    def _xTimeGetter(self, mainInput, miscInputs, fit, tgt, timeCachePrepFunc, timeCacheGetFunc):
        xs = []
        ys = []
        minTime, maxTime = mainInput[1]
        tgtSigRadius = tgt.ship.getModifiedItemAttr('signatureRadius')
        # Process inputs into more convenient form
        miscInputMap = dict(miscInputs)
        # Get all data we need for all times into maps/caches
        applicationMap = self._getApplicationPerKey(
            fit=fit,
            tgt=tgt,
            atkSpeed=miscInputMap['atkSpeed'],
            atkAngle=miscInputMap['atkAngle'],
            distance=miscInputMap['distance'],
            tgtSpeed=miscInputMap['tgtSpeed'],
            tgtAngle=miscInputMap['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        timeCachePrepFunc(fit, maxTime)
        timeCache = timeCacheGetFunc(fit)
        # Custom iteration for time graph to show all data points
        currentDmg = None
        currentTime = None
        for currentTime in sorted(timeCache):
            prevDmg = currentDmg
            currentDmgData = timeCache[currentTime]
            currentDmg = self._aggregate(dmgMap=currentDmgData, applicationMap=applicationMap).total
            if currentTime < minTime:
                continue
            # First set of data points
            if not xs:
                # Start at exactly requested time, at last known value
                initialDmg = prevDmg or 0
                xs.append(minTime)
                ys.append(initialDmg)
                # If current time is bigger then starting, extend plot to that time with old value
                if currentTime > minTime:
                    xs.append(currentTime)
                    ys.append(initialDmg)
                # If new value is different, extend it with new point to the new value
                if currentDmg != prevDmg:
                    xs.append(currentTime)
                    ys.append(currentDmg)
                continue
            # Last data point
            if currentTime >= maxTime:
                xs.append(maxTime)
                ys.append(prevDmg)
                break
            # Anything in-between
            if currentDmg != prevDmg:
                if prevDmg is not None:
                    xs.append(currentTime)
                    ys.append(prevDmg)
                xs.append(currentTime)
                ys.append(currentDmg)
        if maxTime > (currentTime or 0):
            xs.append(maxTime)
            ys.append(currentDmg or 0)
        return xs, ys

    def _xTgtSpeedGetter(self, mainInput, miscInputs, fit, tgt, dmgFunc, timeCachePrepFunc):
        xs = []
        ys = []
        tgtSigRadius = tgt.ship.getModifiedItemAttr('signatureRadius')
        # Process inputs into more convenient form
        miscInputMap = dict(miscInputs)
        # Get all data we need for all target speeds into maps/caches
        timeCachePrepFunc(fit, miscInputMap['time'])
        dmgMap = dmgFunc(fit=fit, time=miscInputMap['time'])
        # Go through target speeds and calculate distance-dependent data
        for tgtSpeed in self._iterLinear(mainInput[1]):
            applicationMap = self._getApplicationPerKey(
                fit=fit,
                tgt=tgt,
                atkSpeed=miscInputMap['atkSpeed'],
                atkAngle=miscInputMap['atkAngle'],
                distance=miscInputMap['distance'],
                tgtSpeed=tgtSpeed,
                tgtAngle=miscInputMap['tgtAngle'],
                tgtSigRadius=tgtSigRadius)
            dmg = self._aggregate(dmgMap=dmgMap, applicationMap=applicationMap).total
            xs.append(tgtSpeed)
            ys.append(dmg)
        return xs, ys

    def _xTgtSigRadiusGetter(self, mainInput, miscInputs, fit, tgt, dmgFunc, timeCachePrepFunc):
        xs = []
        ys = []
        # Process inputs into more convenient form
        miscInputMap = dict(miscInputs)
        # Get all data we need for all target speeds into maps/caches
        timeCachePrepFunc(fit, miscInputMap['time'])
        dmgMap = dmgFunc(fit=fit, time=miscInputMap['time'])
        # Go through target speeds and calculate distance-dependent data
        for tgtSigRadius in self._iterLinear(mainInput[1]):
            applicationMap = self._getApplicationPerKey(
                fit=fit,
                tgt=tgt,
                atkSpeed=miscInputMap['atkSpeed'],
                atkAngle=miscInputMap['atkAngle'],
                distance=miscInputMap['distance'],
                tgtSpeed=miscInputMap['tgtSpeed'],
                tgtAngle=miscInputMap['tgtAngle'],
                tgtSigRadius=tgtSigRadius)
            dmg = self._aggregate(dmgMap=dmgMap, applicationMap=applicationMap).total
            xs.append(tgtSigRadius)
            ys.append(dmg)
        return xs, ys

    # Damage data per key getters
    def _getDpsPerKey(self, fit, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._timeCache.getDpsDataPoint(fit, time)
        # Compose map ourselves using current fit settings if time is not specified
        dpsMap = {}
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        for mod in fit.modules:
            if not mod.isDealingDamage():
                continue
            dpsMap[mod] = mod.getDps(spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False))
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            dpsMap[drone] = drone.getDps()
        for fighter in fit.fighters:
            if not fighter.isDealingDamage():
                continue
            for effectID, effectDps in fighter.getDpsPerEffect().items():
                dpsMap[(fighter, effectID)] = effectDps
        return dpsMap

    def _getVolleyPerKey(self, fit, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._timeCache.getVolleyDataPoint(fit, time)
        # Compose map ourselves using current fit settings if time is not specified
        volleyMap = {}
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        for mod in fit.modules:
            if not mod.isDealingDamage():
                continue
            volleyMap[mod] = mod.getVolley(spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False))
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            volleyMap[drone] = drone.getVolley()
        for fighter in fit.fighters:
            if not fighter.isDealingDamage():
                continue
            for effectID, effectVolley in fighter.getVolleyPerEffect().items():
                volleyMap[(fighter, effectID)] = effectVolley
        return volleyMap

    def _getDmgPerKey(self, fit, time):
        # Damage inflicted makes no sense without time specified
        if time is None:
            raise ValueError
        return self._timeCache.getDmgDataPoint(fit, time)

    # Application getter
    def _getApplicationPerKey(self, fit, tgt, atkSpeed, atkAngle, distance, tgtSpeed, tgtAngle, tgtSigRadius):
        applicationMap = {}
        for mod in fit.modules:
            if not mod.isDealingDamage():
                continue
            if mod.hardpoint == FittingHardpoint.TURRET:
                applicationMap[mod] = getTurretMult(
                    mod=mod,
                    fit=fit,
                    tgt=tgt,
                    atkSpeed=atkSpeed,
                    atkAngle=atkAngle,
                    distance=distance,
                    tgtSpeed=tgtSpeed,
                    tgtAngle=tgtAngle,
                    tgtSigRadius=tgtSigRadius)
            elif mod.hardpoint == FittingHardpoint.MISSILE:
                applicationMap[mod] = getLauncherMult(
                    mod=mod,
                    fit=fit,
                    distance=distance,
                    tgtSpeed=tgtSpeed,
                    tgtSigRadius=tgtSigRadius)
            elif mod.item.group.name in ('Smart Bomb', 'Structure Area Denial Module'):
                applicationMap[mod] = getSmartbombMult(
                    mod=mod,
                    distance=distance)
            elif mod.item.group.name == 'Missile Launcher Bomb':
                applicationMap[mod] = getBombMult(
                    mod=mod,
                    fit=fit,
                    tgt=tgt,
                    distance=distance,
                    tgtSigRadius=tgtSigRadius)
            elif mod.item.group.name == 'Structure Guided Bomb Launcher':
                applicationMap[mod] = getGuidedBombMult(
                    mod=mod,
                    fit=fit,
                    distance=distance,
                    tgtSigRadius=tgtSigRadius)
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            applicationMap[drone] = getDroneMult(
                drone=drone,
                fit=fit,
                tgt=tgt,
                atkSpeed=atkSpeed,
                atkAngle=atkAngle,
                distance=distance,
                tgtSpeed=tgtSpeed,
                tgtAngle=tgtAngle,
                tgtSigRadius=tgtSigRadius)
        for fighter in fit.fighters:
            if not fighter.isDealingDamage():
                continue
            for ability in fighter.abilities:
                if not ability.dealsDamage or not ability.active:
                    continue
                applicationMap[(fighter, ability.effectID)] = getFighterAbilityMult(
                    fighter=fighter,
                    ability=ability,
                    fit=fit,
                    distance=distance,
                    tgtSpeed=tgtSpeed,
                    tgtSigRadius=tgtSigRadius)
        return applicationMap

    # Calculate damage from maps
    def _aggregate(self, dmgMap, applicationMap):
        total = DmgTypes(0, 0, 0, 0)
        for key, dmg in dmgMap.items():
            total += dmg * applicationMap.get(key, 0)
        return total


FitDamageStatsGraph.register()
