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
from eos.const import FittingHardpoint, FittingModuleState
from eos.utils.float import floatUnerr
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from gui.builtinGraphs.base import FitGraph, XDef, YDef, Input, VectorDef
from .calc import getTurretMult, getLauncherMult, getDroneMult, getFighterAbilityMult
from .timeCache import TimeCache


class FitDamageStatsGraph(FitGraph):

    def __init__(self):
        super().__init__()
        self._timeCache = TimeCache()

    def _clearInternalCache(self, fitID):
        self._timeCache.clear(fitID)

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
        xs = []
        ys = []
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        miscInputMap = dict(miscInputs)
        tgtSigRad = miscInputMap.get('tgtSigRad', tgt.ship.getModifiedItemAttr('signatureRadius'))
        for distance in self._iterLinear(mainInput[1]):
            totalDps = 0
            for mod in fit.modules:
                if not mod.isDealingDamage():
                    continue
                modDps = mod.getDps(spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False)).total
                if mod.hardpoint == FittingHardpoint.TURRET:
                    if mod.state >= FittingModuleState.ACTIVE:
                        totalDps += modDps * getTurretMult(
                            mod=mod,
                            fit=fit,
                            tgt=tgt,
                            atkSpeed=miscInputMap['atkSpeed'],
                            atkAngle=miscInputMap['atkAngle'],
                            distance=distance,
                            tgtSpeed=miscInputMap['tgtSpeed'],
                            tgtAngle=miscInputMap['tgtAngle'],
                            tgtSigRadius=tgtSigRad)
                elif mod.hardpoint == FittingHardpoint.MISSILE:
                    if mod.state >= FittingModuleState.ACTIVE:
                        totalDps += modDps * getLauncherMult(
                            mod=mod,
                            fit=fit,
                            distance=distance,
                            tgtSpeed=miscInputMap['tgtSpeed'],
                            tgtSigRadius=tgtSigRad)
            for drone in fit.drones:
                if not drone.isDealingDamage():
                    continue
                droneDps = drone.getDps().total
                totalDps += droneDps * getDroneMult(
                    drone=drone,
                    fit=fit,
                    tgt=tgt,
                    atkSpeed=miscInputMap['atkSpeed'],
                    atkAngle=miscInputMap['atkAngle'],
                    distance=distance,
                    tgtSpeed=miscInputMap['tgtSpeed'],
                    tgtAngle=miscInputMap['tgtAngle'],
                    tgtSigRadius=tgtSigRad)
            for fighter in fit.fighters:
                if not fighter.isDealingDamage():
                    continue
                abilityMap = fighter.abilityMap
                for effectID, abilityDps in fighter.getDpsPerEffect().items():
                    ability = abilityMap[effectID]
                    totalDps += abilityDps.total * getFighterAbilityMult(
                        fighter=fighter,
                        ability=ability,
                        fit=fit,
                        distance=distance,
                        tgtSpeed=miscInputMap['tgtSpeed'],
                        tgtSigRadius=tgtSigRad)
            xs.append(distance)
            ys.append(totalDps)
        return xs, ys

    def _distance2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2dps(self, mainInput, miscInputs, fit, tgt):
        def calcDpsTmp(timeDmg):
            return floatUnerr(sum(dts.total for dts in timeDmg.values()))
        self._timeCache.prepareDpsData(fit, mainInput[1][1])
        return self._composeTimeGraph(mainInput, fit, self._timeCache.getDpsData, calcDpsTmp)

    def _time2volley(self, mainInput, miscInputs, fit, tgt):
        def calcVolleyTmp(timeDmg):
            return floatUnerr(sum(dts.total for dts in timeDmg.values()))
        self._timeCache.prepareVolleyData(fit, mainInput[1][1])
        return self._composeTimeGraph(mainInput, fit, self._timeCache.getVolleyData, calcVolleyTmp)

    def _time2damage(self, mainInput, miscInputs, fit, tgt):
        def calcDamageTmp(timeDmg):
            return floatUnerr(sum(dt.total for dt in timeDmg.values()))
        self._timeCache.prepareDmgData(fit, mainInput[1][1])
        return self._composeTimeGraph(mainInput, fit, self._timeCache.getDmgData, calcDamageTmp)

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

    def _composeTimeGraph(self, mainInput, fit, cacheFunc, calcFunc):
        xs = []
        ys = []

        minTime, maxTime = mainInput[1]
        cache = cacheFunc(fit)
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


FitDamageStatsGraph.register()
