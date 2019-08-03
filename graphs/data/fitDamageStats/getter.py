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
from .calc.projected import getTpMult, getWebbedSpeed
from .helper import getTgtSigRadius


def applyDamage(dmgMap, applicationMap):
    total = DmgTypes(0, 0, 0, 0)
    for key, dmg in dmgMap.items():
        total += dmg * applicationMap.get(key, 0)
    return total


# Y mixins
class YDpsMixin:

    def _getDamagePerKey(self, fit, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._getTimeCacheDataPoint(fit=fit, time=time)
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

    def _prepareTimeCache(self, fit, maxTime):
        self.graph._timeCache.prepareDpsData(fit=fit, maxTime=maxTime)

    def _getTimeCacheData(self, fit):
        return self.graph._timeCache.getDpsData(fit=fit)

    def _getTimeCacheDataPoint(self, fit, time):
        return self.graph._timeCache.getDpsDataPoint(fit=fit, time=time)


class YVolleyMixin:

    def _getDamagePerKey(self, fit, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._getTimeCacheDataPoint(fit=fit, time=time)
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

    def _prepareTimeCache(self, fit, maxTime):
        self.graph._timeCache.prepareVolleyData(fit=fit, maxTime=maxTime)

    def _getTimeCacheData(self, fit):
        return self.graph._timeCache.getVolleyData(fit=fit)

    def _getTimeCacheDataPoint(self, fit, time):
        return self.graph._timeCache.getVolleyDataPoint(fit=fit, time=time)


class YInflictedDamageMixin:

    def _getDamagePerKey(self, fit, time):
        # Damage inflicted makes no sense without time specified
        if time is None:
            raise ValueError
        return self._getTimeCacheDataPoint(fit=fit, time=time)

    def _prepareTimeCache(self, fit, maxTime):
        self.graph._timeCache.prepareDmgData(fit=fit, maxTime=maxTime)

    def _getTimeCacheData(self, fit):
        return self.graph._timeCache.getDmgData(fit=fit)

    def _getTimeCacheDataPoint(self, fit, time):
        return self.graph._timeCache.getDmgDataPoint(fit=fit, time=time)


# X mixins
class XDistanceMixin(SmoothPointGetter):

    def _getCommonData(self, miscParams, fit, tgt):
        # Process params into more convenient form
        miscParamMap = dict(miscParams)
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(fit=fit, maxTime=miscParamMap['time'])
        return {
            'applyProjected': GraphSettings.getInstance().get('applyProjected'),
            'miscParamMap': miscParamMap,
            'dmgMap': self._getDamagePerKey(fit=fit, time=miscParamMap['time'])}

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        distance = x
        miscParamMap = commonData['miscParamMap']
        tgtSpeed = miscParamMap['tgtSpeed']
        tgtSigRadius = getTgtSigRadius(tgt)
        if commonData['applyProjected']:
            webMods, tpMods = self.graph._projectedCache.getProjModData(fit)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(fit)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(fit)
            tgtSpeed = getWebbedSpeed(
                fit=fit,
                tgt=tgt,
                currentUnwebbedSpeed=tgtSpeed,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=distance)
            tgtSigRadius = tgtSigRadius * getTpMult(
                fit=fit,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=distance)
        applicationMap = getApplicationPerKey(
            fit=fit,
            tgt=tgt,
            atkSpeed=miscParamMap['atkSpeed'],
            atkAngle=miscParamMap['atkAngle'],
            distance=distance,
            tgtSpeed=tgtSpeed,
            tgtAngle=miscParamMap['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        y = applyDamage(dmgMap=commonData['dmgMap'], applicationMap=applicationMap).total
        return y


class XTimeMixin(PointGetter):

    def _prepareApplicationMap(self, miscParams, fit, tgt):
        # Process params into more convenient form
        miscParamMap = dict(miscParams)
        tgtSpeed = miscParamMap['tgtSpeed']
        tgtSigRadius = getTgtSigRadius(tgt)
        if GraphSettings.getInstance().get('applyProjected'):
            webMods, tpMods = self.graph._projectedCache.getProjModData(fit)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(fit)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(fit)
            tgtSpeed = getWebbedSpeed(
                fit=fit,
                tgt=tgt,
                currentUnwebbedSpeed=tgtSpeed,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=miscParamMap['distance'])
            tgtSigRadius = tgtSigRadius * getTpMult(
                fit=fit,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=miscParamMap['distance'])
        # Get all data we need for all times into maps/caches
        applicationMap = getApplicationPerKey(
            fit=fit,
            tgt=tgt,
            atkSpeed=miscParamMap['atkSpeed'],
            atkAngle=miscParamMap['atkAngle'],
            distance=miscParamMap['distance'],
            tgtSpeed=tgtSpeed,
            tgtAngle=miscParamMap['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        return applicationMap

    def getRange(self, xRange, miscParams, fit, tgt):
        xs = []
        ys = []
        minTime, maxTime = xRange
        # Prepare time cache and various shared data
        self._prepareTimeCache(fit=fit, maxTime=maxTime)
        timeCache = self._getTimeCacheData(fit=fit)
        applicationMap = self._prepareApplicationMap(miscParams=miscParams, fit=fit, tgt=tgt)
        # Custom iteration for time graph to show all data points
        currentDmg = None
        currentTime = None
        for currentTime in sorted(timeCache):
            prevDmg = currentDmg
            currentDmgData = timeCache[currentTime]
            currentDmg = applyDamage(dmgMap=currentDmgData, applicationMap=applicationMap).total
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

    def getPoint(self, x, miscParams, fit, tgt):
        time = x
        # Prepare time cache and various data
        self._prepareTimeCache(fit=fit, maxTime=time)
        dmgData = self._getTimeCacheDataPoint(fit=fit, time=time)
        applicationMap = self._prepareApplicationMap(miscParams=miscParams, fit=fit, tgt=tgt)
        y = applyDamage(dmgMap=dmgData, applicationMap=applicationMap).total
        return y


class XTgtSpeedMixin(SmoothPointGetter):

    def _getCommonData(self, miscParams, fit, tgt):
        # Process params into more convenient form
        miscParamMap = dict(miscParams)
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(fit=fit, maxTime=miscParamMap['time'])
        return {
            'applyProjected': GraphSettings.getInstance().get('applyProjected'),
            'miscParamMap': miscParamMap,
            'dmgMap': self._getDamagePerKey(fit=fit, time=miscParamMap['time'])}

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        tgtSpeed = x
        miscParamMap = commonData['miscParamMap']
        tgtSigRadius = getTgtSigRadius(tgt)
        if commonData['applyProjected']:
            webMods, tpMods = self.graph._projectedCache.getProjModData(fit)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(fit)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(fit)
            tgtSpeed = getWebbedSpeed(
                fit=fit,
                tgt=tgt,
                currentUnwebbedSpeed=tgtSpeed,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=miscParamMap['distance'])
            tgtSigRadius = tgtSigRadius * getTpMult(
                fit=fit,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=miscParamMap['distance'])
        applicationMap = getApplicationPerKey(
            fit=fit,
            tgt=tgt,
            atkSpeed=miscParamMap['atkSpeed'],
            atkAngle=miscParamMap['atkAngle'],
            distance=miscParamMap['distance'],
            tgtSpeed=tgtSpeed,
            tgtAngle=miscParamMap['tgtAngle'],
            tgtSigRadius=tgtSigRadius)
        y = applyDamage(dmgMap=commonData['dmgMap'], applicationMap=applicationMap).total
        return y


class XTgtSigRadiusMixin(SmoothPointGetter):

    def _getCommonData(self, miscParams, fit, tgt):
        # Process params into more convenient form
        miscParamMap = dict(miscParams)
        tgtSpeed = miscParamMap['tgtSpeed']
        tgtSigMult = 1
        if GraphSettings.getInstance().get('applyProjected'):
            webMods, tpMods = self.graph._projectedCache.getProjModData(fit)
            webDrones, tpDrones = self.graph._projectedCache.getProjDroneData(fit)
            webFighters, tpFighters = self.graph._projectedCache.getProjFighterData(fit)
            tgtSpeed = getWebbedSpeed(
                fit=fit,
                tgt=tgt,
                currentUnwebbedSpeed=tgtSpeed,
                webMods=webMods,
                webDrones=webDrones,
                webFighters=webFighters,
                distance=miscParamMap['distance'])
            tgtSigMult = getTpMult(
                fit=fit,
                tgt=tgt,
                tgtSpeed=tgtSpeed,
                tpMods=tpMods,
                tpDrones=tpDrones,
                tpFighters=tpFighters,
                distance=miscParamMap['distance'])
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(fit=fit, maxTime=miscParamMap['time'])
        return {
            'miscParamMap': miscParamMap,
            'tgtSpeed': tgtSpeed,
            'tgtSigMult': tgtSigMult,
            'dmgMap': self._getDamagePerKey(fit=fit, time=miscParamMap['time'])}

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        tgtSigRadius = x
        miscParamMap = commonData['miscParamMap']
        applicationMap = getApplicationPerKey(
            fit=fit,
            tgt=tgt,
            atkSpeed=miscParamMap['atkSpeed'],
            atkAngle=miscParamMap['atkAngle'],
            distance=miscParamMap['distance'],
            tgtSpeed=commonData['tgtSpeed'],
            tgtAngle=miscParamMap['tgtAngle'],
            tgtSigRadius=tgtSigRadius * commonData['tgtSigMult'])
        y = applyDamage(dmgMap=commonData['dmgMap'], applicationMap=applicationMap).total
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
