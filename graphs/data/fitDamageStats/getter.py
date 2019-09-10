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
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from eos.utils.stats import DmgTypes
from graphs.data.base import PointGetter, SmoothPointGetter
from service.settings import GraphSettings
from .calc.application import getApplicationPerKey
from .calc.projected import getScramRange, getScrammables, getTackledSpeed, getSigRadiusMult


def applyDamage(dmgMap, applicationMap, tgtResists):
    total = DmgTypes(em=0, thermal=0, kinetic=0, explosive=0)
    for key, dmg in dmgMap.items():
        total += dmg * applicationMap.get(key, 0)
    if not GraphSettings.getInstance().get('ignoreResists'):
        emRes, thermRes, kinRes, exploRes = tgtResists
        total = DmgTypes(
            em=total.em * (1 - emRes),
            thermal=total.thermal * (1 - thermRes),
            kinetic=total.kinetic * (1 - kinRes),
            explosive=total.explosive * (1 - exploRes))
    return total


# Y mixins
class YDpsMixin:

    def _getDamagePerKey(self, src, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._getTimeCacheDataPoint(src=src, time=time)
        # Compose map ourselves using current fit settings if time is not specified
        dpsMap = {}
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        for mod in src.item.activeModulesIter():
            if not mod.isDealingDamage():
                continue
            dpsMap[mod] = mod.getDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False))
        for drone in src.item.activeDronesIter():
            if not drone.isDealingDamage():
                continue
            dpsMap[drone] = drone.getDps()
        for fighter in src.item.activeFightersIter():
            if not fighter.isDealingDamage():
                continue
            for effectID, effectDps in fighter.getDpsPerEffect().items():
                dpsMap[(fighter, effectID)] = effectDps
        return dpsMap

    def _prepareTimeCache(self, src, maxTime):
        self.graph._timeCache.prepareDpsData(src=src, maxTime=maxTime)

    def _getTimeCacheData(self, src):
        return self.graph._timeCache.getDpsData(src=src)

    def _getTimeCacheDataPoint(self, src, time):
        return self.graph._timeCache.getDpsDataPoint(src=src, time=time)


class YVolleyMixin:

    def _getDamagePerKey(self, src, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._getTimeCacheDataPoint(src=src, time=time)
        # Compose map ourselves using current fit settings if time is not specified
        volleyMap = {}
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        for mod in src.item.activeModulesIter():
            if not mod.isDealingDamage():
                continue
            volleyMap[mod] = mod.getVolley(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False))
        for drone in src.item.activeDronesIter():
            if not drone.isDealingDamage():
                continue
            volleyMap[drone] = drone.getVolley()
        for fighter in src.item.activeFightersIter():
            if not fighter.isDealingDamage():
                continue
            for effectID, effectVolley in fighter.getVolleyPerEffect().items():
                volleyMap[(fighter, effectID)] = effectVolley
        return volleyMap

    def _prepareTimeCache(self, src, maxTime):
        self.graph._timeCache.prepareVolleyData(src=src, maxTime=maxTime)

    def _getTimeCacheData(self, src):
        return self.graph._timeCache.getVolleyData(src=src)

    def _getTimeCacheDataPoint(self, src, time):
        return self.graph._timeCache.getVolleyDataPoint(src=src, time=time)


class YInflictedDamageMixin:

    def _getDamagePerKey(self, src, time):
        # Damage inflicted makes no sense without time specified
        if time is None:
            raise ValueError
        return self._getTimeCacheDataPoint(src=src, time=time)

    def _prepareTimeCache(self, src, maxTime):
        self.graph._timeCache.prepareDmgData(src=src, maxTime=maxTime)

    def _getTimeCacheData(self, src):
        return self.graph._timeCache.getDmgData(src=src)

    def _getTimeCacheDataPoint(self, src, time):
        return self.graph._timeCache.getDmgDataPoint(src=src, time=time)


# X mixins
class XDistanceMixin(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(src=src, maxTime=miscParams['time'])
        applyProjected = GraphSettings.getInstance().get('applyProjected')
        return {
            'applyProjected': applyProjected,
            'srcScramRange': getScramRange(src=src) if applyProjected else None,
            'tgtScrammables': getScrammables(tgt=tgt) if applyProjected else (),
            'dmgMap': self._getDamagePerKey(src=src, time=miscParams['time']),
            'tgtResists': tgt.getResists()}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        tgtSpeed = miscParams['tgtSpeed']
        tgtSigRadius = tgt.getSigRadius()
        if commonData['applyProjected']:
            webMods, tpMods = self.graph._projectedCache.getProjModData(src)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(src)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(src)
            tgtSpeed = getTackledSpeed(
                src=src,
                tgt=tgt,
                currentUntackledSpeed=tgtSpeed,
                srcScramRange=commonData['srcScramRange'],
                tgtScrammables=commonData['tgtScrammables'],
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=distance)
            tgtSigRadius = tgtSigRadius * getSigRadiusMult(
                src=src,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                srcScramRange=commonData['srcScramRange'],
                tgtScrammables=commonData['tgtScrammables'],
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=distance)
        applicationMap = getApplicationPerKey(
            src=src,
            tgt=tgt,
            atkSpeed=miscParams['atkSpeed'],
            atkAngle=miscParams['atkAngle'],
            distance=distance,
            tgtSpeed=tgtSpeed,
            tgtAngle=miscParams['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        y = applyDamage(
            dmgMap=commonData['dmgMap'],
            applicationMap=applicationMap,
            tgtResists=commonData['tgtResists']).total
        return y


class XTimeMixin(PointGetter):

    def _prepareApplicationMap(self, miscParams, src, tgt):
        tgtSpeed = miscParams['tgtSpeed']
        tgtSigRadius = tgt.getSigRadius()
        if GraphSettings.getInstance().get('applyProjected'):
            srcScramRange = getScramRange(src=src)
            tgtScrammables = getScrammables(tgt=tgt)
            webMods, tpMods = self.graph._projectedCache.getProjModData(src)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(src)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(src)
            tgtSpeed = getTackledSpeed(
                src=src,
                tgt=tgt,
                currentUntackledSpeed=tgtSpeed,
                srcScramRange=srcScramRange,
                tgtScrammables=tgtScrammables,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=miscParams['distance'])
            tgtSigRadius = tgtSigRadius * getSigRadiusMult(
                src=src,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                srcScramRange=srcScramRange,
                tgtScrammables=tgtScrammables,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=miscParams['distance'])
        # Get all data we need for all times into maps/caches
        applicationMap = getApplicationPerKey(
            src=src,
            tgt=tgt,
            atkSpeed=miscParams['atkSpeed'],
            atkAngle=miscParams['atkAngle'],
            distance=miscParams['distance'],
            tgtSpeed=tgtSpeed,
            tgtAngle=miscParams['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        return applicationMap

    def getRange(self, xRange, miscParams, src, tgt):
        xs = []
        ys = []
        minTime, maxTime = xRange
        # Prepare time cache and various shared data
        self._prepareTimeCache(src=src, maxTime=maxTime)
        timeCache = self._getTimeCacheData(src=src)
        applicationMap = self._prepareApplicationMap(miscParams=miscParams, src=src, tgt=tgt)
        tgtResists = tgt.getResists()
        # Custom iteration for time graph to show all data points
        currentDmg = None
        currentTime = None
        for currentTime in sorted(timeCache):
            prevDmg = currentDmg
            currentDmgData = timeCache[currentTime]
            currentDmg = applyDamage(dmgMap=currentDmgData, applicationMap=applicationMap, tgtResists=tgtResists).total
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
        # Special case - there are no damage dealers
        if currentDmg is None and currentTime is None:
            xs.append(minTime)
            ys.append(0)
        # Make sure that last data point is always at max time
        if maxTime > (currentTime or 0):
            xs.append(maxTime)
            ys.append(currentDmg or 0)
        return xs, ys

    def getPoint(self, x, miscParams, src, tgt):
        time = x
        # Prepare time cache and various data
        self._prepareTimeCache(src=src, maxTime=time)
        dmgData = self._getTimeCacheDataPoint(src=src, time=time)
        applicationMap = self._prepareApplicationMap(miscParams=miscParams, src=src, tgt=tgt)
        y = applyDamage(dmgMap=dmgData, applicationMap=applicationMap, tgtResists=tgt.getResists()).total
        return y


class XTgtSpeedMixin(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(src=src, maxTime=miscParams['time'])
        return {
            'applyProjected': GraphSettings.getInstance().get('applyProjected'),
            'dmgMap': self._getDamagePerKey(src=src, time=miscParams['time']),
            'tgtResists': tgt.getResists()}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        tgtSpeed = x
        tgtSigRadius = tgt.getSigRadius()
        if commonData['applyProjected']:
            srcScramRange = getScramRange(src=src)
            tgtScrammables = getScrammables(tgt=tgt)
            webMods, tpMods = self.graph._projectedCache.getProjModData(src)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(src)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(src)
            tgtSpeed = getTackledSpeed(
                src=src,
                tgt=tgt,
                currentUntackledSpeed=tgtSpeed,
                srcScramRange=srcScramRange,
                tgtScrammables=tgtScrammables,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=miscParams['distance'])
            tgtSigRadius = tgtSigRadius * getSigRadiusMult(
                src=src,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                srcScramRange=srcScramRange,
                tgtScrammables=tgtScrammables,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=miscParams['distance'])
        applicationMap = getApplicationPerKey(
            src=src,
            tgt=tgt,
            atkSpeed=miscParams['atkSpeed'],
            atkAngle=miscParams['atkAngle'],
            distance=miscParams['distance'],
            tgtSpeed=tgtSpeed,
            tgtAngle=miscParams['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        y = applyDamage(
            dmgMap=commonData['dmgMap'],
            applicationMap=applicationMap,
            tgtResists=commonData['tgtResists']).total
        return y


class XTgtSigRadiusMixin(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        tgtSpeed = miscParams['tgtSpeed']
        tgtSigMult = 1
        if GraphSettings.getInstance().get('applyProjected'):
            srcScramRange = getScramRange(src=src)
            tgtScrammables = getScrammables(tgt=tgt)
            webMods, tpMods = self.graph._projectedCache.getProjModData(src)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(src)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(src)
            tgtSpeed = getTackledSpeed(
                src=src,
                tgt=tgt,
                currentUntackledSpeed=tgtSpeed,
                srcScramRange=srcScramRange,
                tgtScrammables=tgtScrammables,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=miscParams['distance'])
            tgtSigMult = getSigRadiusMult(
                src=src,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                srcScramRange=srcScramRange,
                tgtScrammables=tgtScrammables,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=miscParams['distance'])
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(src=src, maxTime=miscParams['time'])
        return {
            'tgtSpeed': tgtSpeed,
            'tgtSigMult': tgtSigMult,
            'dmgMap': self._getDamagePerKey(src=src, time=miscParams['time']),
            'tgtResists': tgt.getResists()}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        tgtSigRadius = x
        applicationMap = getApplicationPerKey(
            src=src,
            tgt=tgt,
            atkSpeed=miscParams['atkSpeed'],
            atkAngle=miscParams['atkAngle'],
            distance=miscParams['distance'],
            tgtSpeed=commonData['tgtSpeed'],
            tgtAngle=miscParams['tgtAngle'],
            tgtSigRadius=tgtSigRadius * commonData['tgtSigMult'])
        y = applyDamage(
            dmgMap=commonData['dmgMap'],
            applicationMap=applicationMap,
            tgtResists=commonData['tgtResists']).total
        return y


# Final getters
class Distance2DpsGetter(XDistanceMixin, YDpsMixin):
    pass


class Distance2VolleyGetter(XDistanceMixin, YVolleyMixin):
    pass


class Distance2InflictedDamageGetter(XDistanceMixin, YInflictedDamageMixin):
    pass


class Time2DpsGetter(XTimeMixin, YDpsMixin):
    pass


class Time2VolleyGetter(XTimeMixin, YVolleyMixin):
    pass


class Time2InflictedDamageGetter(XTimeMixin, YInflictedDamageMixin):
    pass


class TgtSpeed2DpsGetter(XTgtSpeedMixin, YDpsMixin):
    pass


class TgtSpeed2VolleyGetter(XTgtSpeedMixin, YVolleyMixin):
    pass


class TgtSpeed2InflictedDamageGetter(XTgtSpeedMixin, YInflictedDamageMixin):
    pass


class TgtSigRadius2DpsGetter(XTgtSigRadiusMixin, YDpsMixin):
    pass


class TgtSigRadius2VolleyGetter(XTgtSigRadiusMixin, YVolleyMixin):
    pass


class TgtSigRadius2InflictedDamageGetter(XTgtSigRadiusMixin, YInflictedDamageMixin):
    pass
