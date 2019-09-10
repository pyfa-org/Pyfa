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
from eos.utils.stats import RRTypes
from graphs.data.base import PointGetter, SmoothPointGetter
from .calc import getApplicationPerKey


def applyReps(rrMap, applicationMap):
    totalAmount = RRTypes(shield=0, armor=0, hull=0, capacitor=0)
    for key, repAmount in rrMap.items():
        totalAmount += repAmount * applicationMap.get(key, 0)
    # We do not want to include energy transfers into final value
    totalReps = totalAmount.shield + totalAmount.armor + totalAmount.hull
    return totalReps


# Y mixins
class YRpsMixin:

    def _getRepsPerKey(self, src, ancReload, time):
        # Use data from time cache if time was not specified
        if time is not None:
            return self._getTimeCacheDataPoint(src=src, ancReload=ancReload, time=time)
        # Compose map ourselves using current fit settings if time is not specified
        rpsMap = {}
        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        for mod in src.item.activeModulesIter():
            if not mod.isRemoteRepping():
                continue
            isAncShield = 'shipModuleAncillaryRemoteShieldBooster' in mod.item.effects
            isAncArmor = 'shipModuleAncillaryRemoteArmorRepairer' in mod.item.effects
            rpsMap[mod] = mod.getRemoteReps(
                spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False),
                reloadOverride=ancReload if (isAncShield or isAncArmor) else None)
        for drone in src.item.activeDronesIter():
            if not drone.isRemoteRepping():
                continue
            rpsMap[drone] = drone.getRemoteReps()
        return rpsMap

    def _prepareTimeCache(self, src, ancReload, maxTime):
        self.graph._timeCache.prepareRpsData(src=src, ancReload=ancReload, maxTime=maxTime)

    def _getTimeCacheData(self, src, ancReload):
        return self.graph._timeCache.getRpsData(src=src, ancReload=ancReload)

    def _getTimeCacheDataPoint(self, src, ancReload, time):
        return self.graph._timeCache.getRpsDataPoint(src=src, ancReload=ancReload, time=time)


class YRepAmountMixin:

    def _getRepsPerKey(self, src, ancReload, time):
        # Total reps given makes no sense without time specified
        if time is None:
            raise ValueError
        return self._getTimeCacheDataPoint(src=src, ancReload=ancReload, time=time)

    def _prepareTimeCache(self, src, ancReload, maxTime):
        self.graph._timeCache.prepareRepAmountData(src=src, ancReload=ancReload, maxTime=maxTime)

    def _getTimeCacheData(self, src, ancReload):
        return self.graph._timeCache.getRepAmountData(src=src, ancReload=ancReload)

    def _getTimeCacheDataPoint(self, src, ancReload, time):
        return self.graph._timeCache.getRepAmountDataPoint(src=src, ancReload=ancReload, time=time)


# X mixins
class XDistanceMixin(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        # Prepare time cache here because we need to do it only once,
        # and this function is called once per point info fetch
        self._prepareTimeCache(src=src, ancReload=miscParams['ancReload'], maxTime=miscParams['time'])
        return {'rrMap': self._getRepsPerKey(src=src, ancReload=miscParams['ancReload'], time=miscParams['time'])}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        applicationMap = getApplicationPerKey(src=src, distance=distance)
        y = applyReps(
            rrMap=commonData['rrMap'],
            applicationMap=applicationMap)
        return y


class XTimeMixin(PointGetter):

    def getRange(self, xRange, miscParams, src, tgt):
        xs = []
        ys = []
        minTime, maxTime = xRange
        # Prepare time cache and various shared data
        self._prepareTimeCache(src=src, ancReload=miscParams['ancReload'], maxTime=maxTime)
        timeCache = self._getTimeCacheData(src=src, ancReload=miscParams['ancReload'])
        applicationMap = getApplicationPerKey(src=src, distance=miscParams['distance'])
        # Custom iteration for time graph to show all data points
        currentRepAmount = None
        currentTime = None
        for currentTime in sorted(timeCache):
            prevRepAmount = currentRepAmount
            currentRepAmountData = timeCache[currentTime]
            currentRepAmount = applyReps(rrMap=currentRepAmountData, applicationMap=applicationMap)
            if currentTime < minTime:
                continue
            # First set of data points
            if not xs:
                # Start at exactly requested time, at last known value
                initialRepAmount = prevRepAmount or 0
                xs.append(minTime)
                ys.append(initialRepAmount)
                # If current time is bigger then starting, extend plot to that time with old value
                if currentTime > minTime:
                    xs.append(currentTime)
                    ys.append(initialRepAmount)
                # If new value is different, extend it with new point to the new value
                if currentRepAmount != prevRepAmount:
                    xs.append(currentTime)
                    ys.append(currentRepAmount)
                continue
            # Last data point
            if currentTime >= maxTime:
                xs.append(maxTime)
                ys.append(prevRepAmount)
                break
            # Anything in-between
            if currentRepAmount != prevRepAmount:
                if prevRepAmount is not None:
                    xs.append(currentTime)
                    ys.append(prevRepAmount)
                xs.append(currentTime)
                ys.append(currentRepAmount)
        # Special case - there are no remote reppers
        if currentRepAmount is None and currentTime is None:
            xs.append(minTime)
            ys.append(0)
        # Make sure that last data point is always at max time
        if maxTime > (currentTime or 0):
            xs.append(maxTime)
            ys.append(currentRepAmount or 0)
        return xs, ys

    def getPoint(self, x, miscParams, src, tgt):
        time = x
        # Prepare time cache and various data
        self._prepareTimeCache(src=src, ancReload=miscParams['ancReload'], maxTime=time)
        repAmountData = self._getTimeCacheDataPoint(src=src, ancReload=miscParams['ancReload'], time=time)
        applicationMap = getApplicationPerKey(src=src, distance=miscParams['distance'])
        y = applyReps(rrMap=repAmountData, applicationMap=applicationMap)
        return y


# Final getters
class Distance2RpsGetter(XDistanceMixin, YRpsMixin):
    pass


class Distance2RepAmountGetter(XDistanceMixin, YRepAmountMixin):
    pass


class Time2RpsGetter(XTimeMixin, YRpsMixin):
    pass


class Time2RepAmountGetter(XTimeMixin, YRepAmountMixin):
    pass
