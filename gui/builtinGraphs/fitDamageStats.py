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
from copy import copy
from itertools import chain

from eos.utils.float import floatUnerr
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from eos.utils.stats import DmgTypes
from .base import FitGraph, XDef, YDef, Input, VectorDef


class FitDamageStatsGraph(FitGraph):

    # UI stuff
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
        ('tgtSigRad', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('signatureRadius')}
    _limiters = {
        'time': lambda fit, tgt: (0, 2500)}
    _denormalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v / 1000,
        ('tgtSpeed', '%'): lambda v, fit, tgt: v * 100 / tgt.ship.getModifiedItemAttr('maxVelocity'),
        ('tgtSigRad', '%'): lambda v, fit, tgt: v * 100 / fit.ship.getModifiedItemAttr('signatureRadius')}

    def _distance2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2dps(self, mainInput, miscInputs, fit, tgt):
        def calcDpsTmp(timeDmg):
            return floatUnerr(sum(dts[0].total for dts in timeDmg.values()))
        self._generateTimeCacheDpsVolley(fit, mainInput[1][1])
        return self._composeTimeGraph(mainInput, fit, 'finalDpsVolley', calcDpsTmp)

    def _time2volley(self, mainInput, miscInputs, fit, tgt):
        def calcVolleyTmp(timeDmg):
            return floatUnerr(sum(dts[1].total for dts in timeDmg.values()))
        self._generateTimeCacheDpsVolley(fit, mainInput[1][1])
        return self._composeTimeGraph(mainInput, fit, 'finalDpsVolley', calcVolleyTmp)

    def _time2damage(self, mainInput, miscInputs, fit, tgt):
        def calcDamageTmp(timeDmg):
            return floatUnerr(sum(dt.total for dt in timeDmg.values()))
        self._generateTimeCacheDmg(fit, mainInput[1][1])
        return self._composeTimeGraph(mainInput, fit, 'finalDmg', calcDamageTmp)

    def _tgtSpeed2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

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

    # Cache generation
    def _generateTimeCacheDpsVolley(self, fit, maxTime):
        # Time is none means that time parameter has to be ignored,
        # we do not need cache for that
        if maxTime is None:
            return True
        self._generateTimeCacheIntermediate(fit, maxTime)
        timeCache = self._calcCache[fit.ID]['timeCache']
        # Final cache has been generated already, don't do anything
        if 'finalDpsVolley' in timeCache:
            return
        # Convert cache from segments with assigned values into points
        # which are located at times when dps/volley values change
        pointCache = {}
        for key, dmgList in timeCache['intermediateDpsVolley'].items():
            pointData = pointCache[key] = {}
            prevDps = None
            prevVolley = None
            prevTimeEnd = None
            for timeStart, timeEnd, dps, volley in dmgList:
                # First item
                if not pointData:
                    pointData[timeStart] = (dps, volley)
                # Gap between items
                elif floatUnerr(prevTimeEnd) < floatUnerr(timeStart):
                    pointData[prevTimeEnd] = (DmgTypes(0, 0, 0, 0), DmgTypes(0, 0, 0, 0))
                    pointData[timeStart] = (dps, volley)
                # Changed value
                elif dps != prevDps or volley != prevVolley:
                    pointData[timeStart] = (dps, volley)
                prevDps = dps
                prevVolley = volley
                prevTimeEnd = timeEnd
        # We have another intermediate form, do not need old one any longer
        del timeCache['intermediateDpsVolley']
        changesByTime = {}
        for key, dmgMap in pointCache.items():
            for time in dmgMap:
                changesByTime.setdefault(time, []).append(key)
        # Here we convert cache to following format:
        # {time: {key: (dps, volley}}
        finalCache = timeCache['finalDpsVolley'] = {}
        timeDmgData = {}
        for time in sorted(changesByTime):
            timeDmgData = copy(timeDmgData)
            for key in changesByTime[time]:
                timeDmgData[key] = pointCache[key][time]
            finalCache[time] = timeDmgData

    def _generateTimeCacheDmg(self, fit, maxTime):
        # Time is none means that time parameter has to be ignored,
        # we do not need cache for that
        if maxTime is None:
            return
        self._generateTimeCacheIntermediate(fit, maxTime)
        timeCache = self._calcCache[fit.ID]['timeCache']
        # Final cache has been generated already, don't do anything
        if 'finalDmg' in timeCache:
            return
        intCache = timeCache['intermediateDmg']
        changesByTime = {}
        for key, dmgMap in intCache.items():
            for time in dmgMap:
                changesByTime.setdefault(time, []).append(key)
        # Here we convert cache to following format:
        # {time: {key: damage done by key at this time}}
        finalCache = timeCache['finalDmg'] = {}
        timeDmgData = {}
        for time in sorted(changesByTime):
            timeDmgData = copy(timeDmgData)
            for key in changesByTime[time]:
                keyDmg = intCache[key][time]
                if key in timeDmgData:
                    timeDmgData[key] = timeDmgData[key] + keyDmg
                else:
                    timeDmgData[key] = keyDmg
            finalCache[time] = timeDmgData
        # We do not need intermediate cache once we have final
        del timeCache['intermediateDmg']

    def _generateTimeCacheIntermediate(self, fit, maxTime):
        if self._isTimeCacheValid(fit, maxTime):
            return
        timeCache = self._calcCache.setdefault(fit.ID, {})['timeCache'] = {'maxTime': maxTime}
        intCacheDpsVolley = timeCache['intermediateDpsVolley'] = {}
        intCacheDmg = timeCache['intermediateDmg'] = {}

        def addDpsVolley(ddKey, addedTimeStart, addedTimeFinish, addedVolleys):
            if not addedVolleys:
                return
            volleySum = sum(addedVolleys, DmgTypes(0, 0, 0, 0))
            if volleySum.total > 0:
                addedDps = volleySum / (addedTimeFinish - addedTimeStart)
                # We can take "just best" volley, no matter target resistances, because all
                # known items have the same damage type ratio throughout their cycle - and
                # applying resistances doesn't change final outcome
                bestVolley = max(addedVolleys, key=lambda v: v.total)
                ddCacheDps = intCacheDpsVolley.setdefault(ddKey, [])
                ddCacheDps.append((addedTimeStart, addedTimeFinish, addedDps, bestVolley))

        def addDmg(ddKey, addedTime, addedDmg):
            if addedDmg.total == 0:
                return
            intCacheDmg.setdefault(ddKey, {})[addedTime] = addedDmg

        # Modules
        for mod in fit.modules:
            if not mod.isDealingDamage():
                continue
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTimeMs, inactiveTimeMs in cycleParams.iterCycles():
                cycleVolleys = []
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTimeMs, volley in volleyParams.items():
                    cycleVolleys.append(volley)
                    addDmg(mod, currentTime + volleyTimeMs / 1000, volley)
                addDpsVolley(mod, currentTime, currentTime + cycleTimeMs / 1000, cycleVolleys)
                if inactiveTimeMs > 0:
                    nonstopCycles = 0
                else:
                    nonstopCycles += 1
                if currentTime > maxTime:
                    break
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
        # Drones
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            volleyParams = drone.getVolleyParameters()
            for cycleTimeMs, inactiveTimeMs in cycleParams.iterCycles():
                cycleVolleys = []
                for volleyTimeMs, volley in volleyParams.items():
                    cycleVolleys.append(volley)
                    addDmg(drone, currentTime + volleyTimeMs / 1000, volley)
                addDpsVolley(drone, currentTime, currentTime + cycleTimeMs / 1000, cycleVolleys)
                if currentTime > maxTime:
                    break
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
        # Fighters
        for fighter in fit.fighters:
            if not fighter.isDealingDamage():
                continue
            cycleParams = fighter.getCycleParametersPerEffectOptimizedDps(reloadOverride=True)
            if cycleParams is None:
                continue
            volleyParams = fighter.getVolleyParametersPerEffect()
            for effectID, abilityCycleParams in cycleParams.items():
                if effectID not in volleyParams:
                    continue
                currentTime = 0
                abilityVolleyParams = volleyParams[effectID]
                for cycleTimeMs, inactiveTimeMs in abilityCycleParams.iterCycles():
                    cycleVolleys = []
                    for volleyTimeMs, volley in abilityVolleyParams.items():
                        cycleVolleys.append(volley)
                        addDmg((fighter, effectID), currentTime + volleyTimeMs / 1000, volley)
                    addDpsVolley((fighter, effectID), currentTime, currentTime + cycleTimeMs / 1000, cycleVolleys)
                    if currentTime > maxTime:
                        break
                    currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000

    def _isTimeCacheValid(self, fit, maxTime):
        try:
            cacheMaxTime = self._calcCache[fit.ID]['timeCache']['maxTime']
        except KeyError:
            return False
        return maxTime <= cacheMaxTime

    def _generateTimeCacheDps(self, fit, maxTime):
        if fit.ID in self._calcCache and 'timeDps' in self._calcCache[fit.ID]:
            return
        intermediateCache = []

        def addDmg(addedTimeStart, addedTimeFinish, addedDmg):
            if addedDmg == 0:
                return
            addedDps = addedDmg / (addedTimeFinish - addedTimeStart)
            intermediateCache.append((addedTimeStart, addedTimeFinish, addedDps))

        for mod in fit.modules:
            if not mod.isDealingDamage():
                continue
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTimeMs, inactiveTimeMs in cycleParams.iterCycles():
                cycleDamage = 0
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTimeMs, volley in volleyParams.items():
                    cycleDamage += volley.total
                addDmg(currentTime, currentTime + cycleTimeMs / 1000, cycleDamage)
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
                if inactiveTimeMs > 0:
                    nonstopCycles = 0
                else:
                    nonstopCycles += 1
                if currentTime > maxTime:
                    break
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            for cycleTimeMs, inactiveTimeMs in cycleParams.iterCycles():
                cycleDamage = 0
                volleyParams = drone.getVolleyParameters()
                for volleyTimeMs, volley in volleyParams.items():
                    cycleDamage += volley.total
                addDmg(currentTime, currentTime + cycleTimeMs / 1000, cycleDamage)
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
                if currentTime > maxTime:
                    break
        for fighter in fit.fighters:
            if not fighter.isDealingDamage():
                continue
            cycleParams = fighter.getCycleParametersPerEffectOptimizedDps(reloadOverride=True)
            if cycleParams is None:
                continue
            volleyParams = fighter.getVolleyParametersPerEffect()
            for effectID, abilityCycleParams in cycleParams.items():
                if effectID not in volleyParams:
                    continue
                abilityVolleyParams = volleyParams[effectID]
                currentTime = 0
                for cycleTimeMs, inactiveTimeMs in abilityCycleParams.iterCycles():
                    cycleDamage = 0
                    for volleyTimeMs, volley in abilityVolleyParams.items():
                        cycleDamage += volley.total
                    addDmg(currentTime, currentTime + cycleTimeMs / 1000, cycleDamage)
                    currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
                    if currentTime > maxTime:
                        break

        # Post-process cache
        finalCache = {}
        for time in sorted(set(chain((i[0] for i in intermediateCache), (i[1] for i in intermediateCache)))):
            entries = (e for e in intermediateCache if e[0] <= time < e[1])
            dps = sum(e[2] for e in entries)
            finalCache[time] = dps
        fitCache = self._calcCache.setdefault(fit.ID, {})
        fitCache['timeDps'] = finalCache

    def _composeTimeGraph(self, mainInput, fit, cacheName, calcFunc):
        xs = []
        ys = []

        minTime, maxTime = mainInput[1]
        cache = self._calcCache[fit.ID]['timeCache'][cacheName]
        currentDps = None
        currentTime = None
        for currentTime in sorted(cache):
            prevDps = currentDps
            currentDps = calcFunc(cache[currentTime])
            if currentTime < minTime:
                continue
            # First set of data points
            if not xs:
                # Start at exactly requested time, at last known value
                initialDps = prevDps or 0
                xs.append(minTime)
                ys.append(initialDps)
                # If current time is bigger then starting, extend plot to that time with old value
                if currentTime > minTime:
                    xs.append(currentTime)
                    ys.append(initialDps)
                # If new value is different, extend it with new point to the new value
                if currentDps != prevDps:
                    xs.append(currentTime)
                    ys.append(currentDps)
                continue
            # Last data point
            if currentTime >= maxTime:
                xs.append(maxTime)
                ys.append(prevDps)
                break
            # Anything in-between
            if currentDps != prevDps:
                if prevDps is not None:
                    xs.append(currentTime)
                    ys.append(prevDps)
                xs.append(currentTime)
                ys.append(currentDps)
        if maxTime > (currentTime or 0):
            xs.append(maxTime)
            ys.append(currentDps or 0)
        return xs, ys


def calculateAngularVelocity(atkSpeed, atkAngle, atkRadius, distance, tgtSpeed, tgtAngle, tgtRadius):
    atkAngle = atkAngle * math.pi / 180
    tgtAngle = tgtAngle * math.pi / 180
    ctcDistance = atkRadius + distance + tgtRadius
    atkSpeedX = atkSpeed * math.cos(atkAngle)
    atkSpeedY = atkSpeed * math.sin(atkAngle)
    tgtSpeedX = tgtSpeed * math.cos(tgtAngle)
    tgtSpeedY = tgtSpeed * math.sin(tgtAngle)
    relSpeed = math.sqrt((atkSpeedX + tgtSpeedX) ** 2 + (atkSpeedY + tgtSpeedY) ** 2)


def calculateRangeFactor(atkOptimalRange, atkFalloffRange, distance):
    return 0.5 ** ((max(0, distance - atkOptimalRange) / atkFalloffRange) ** 2)


def calculateTrackingFactor(atkTracking, atkOptimalSigRadius, angularSpeed, tgtSigRadius):
    return 0.5 ** (((angularSpeed * atkOptimalSigRadius) / (atkTracking * tgtSigRadius)) ** 2)


FitDamageStatsGraph.register()
