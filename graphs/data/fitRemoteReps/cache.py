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


from copy import copy

from eos.utils.float import floatUnerr
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from eos.utils.stats import RRTypes
from graphs.data.base import FitDataCache


class TimeCache(FitDataCache):

    # Whole data getters
    def getRpsData(self, src):
        """Return RPS data in {time: {key: rps}} format."""
        return self._data[src.item.ID]['finalRps']

    def getRepAmountData(self, src):
        """Return rep amount data in {time: {key: amount}} format."""
        return self._data[src.item.ID]['finalRepAmount']

    # Specific data point getters
    def getRpsDataPoint(self, src, time):
        """Get RPS data by specified time in {key: rps} format."""
        return self._getDataPoint(src=src, time=time, dataFunc=self.getRpsData)

    def getRepAmountDataPoint(self, src, time):
        """Get rep amount data by specified time in {key: amount} format."""
        return self._getDataPoint(src=src, time=time, dataFunc=self.getRepAmountData)

    # Preparation functions
    def prepareRpsData(self, src, maxTime):
        # Time is none means that time parameter has to be ignored,
        # we do not need cache for that
        if maxTime is None:
            return True
        self._generateInternalForm(src=src, maxTime=maxTime)
        fitCache = self._data[src.item.ID]
        # Final cache has been generated already, don't do anything
        if 'finalRps' in fitCache:
            return
        # Convert cache from segments with assigned values into points
        # which are located at times when rps value changes
        pointCache = {}
        for key, rpsList in fitCache['internalRps'].items():
            pointData = pointCache[key] = {}
            prevRps = None
            prevTimeEnd = None
            for timeStart, timeEnd, rps in rpsList:
                # First item
                if not pointData:
                    pointData[timeStart] = rps
                # Gap between items
                elif floatUnerr(prevTimeEnd) < floatUnerr(timeStart):
                    pointData[prevTimeEnd] = RRTypes(0, 0, 0, 0)
                    pointData[timeStart] = rps
                # Changed value
                elif rps != prevRps:
                    pointData[timeStart] = rps
                prevRps = rps
                prevTimeEnd = timeEnd
        # We have data in another form, do not need old one any longer
        del fitCache['internalRps']
        changesByTime = {}
        for key, rpsMap in pointCache.items():
            for time in rpsMap:
                changesByTime.setdefault(time, []).append(key)
        # Here we convert cache to following format:
        # {time: {key: rps}
        finalRpsCache = fitCache['finalRps'] = {}
        timeRpsData = {}
        for time in sorted(changesByTime):
            timeRpsData = copy(timeRpsData)
            for key in changesByTime[time]:
                timeRpsData[key] = pointCache[key][time]
            finalRpsCache[time] = timeRpsData

    def prepareRepAmountData(self, src, maxTime):
        # Time is none means that time parameter has to be ignored,
        # we do not need cache for that
        if maxTime is None:
            return
        self._generateInternalForm(src=src, maxTime=maxTime)
        fitCache = self._data[src.item.ID]
        # Final cache has been generated already, don't do anything
        if 'finalRepAmount' in fitCache:
            return
        intCache = fitCache['internalRepAmount']
        changesByTime = {}
        for key, remAmountMap in intCache.items():
            for time in remAmountMap:
                changesByTime.setdefault(time, []).append(key)
        # Here we convert cache to following format:
        # {time: {key: hp repaired by key at this time}}
        finalCache = fitCache['finalRepAmount'] = {}
        timeRepAmountData = {}
        for time in sorted(changesByTime):
            timeRepAmountData = copy(timeRepAmountData)
            for key in changesByTime[time]:
                keyRepAmount = intCache[key][time]
                if key in timeRepAmountData:
                    timeRepAmountData[key] = timeRepAmountData[key] + keyRepAmount
                else:
                    timeRepAmountData[key] = keyRepAmount
            finalCache[time] = timeRepAmountData
        # We do not need internal cache once we have final
        del fitCache['internalRepAmount']

    # Private stuff
    def _generateInternalForm(self, src, maxTime):
        if self._isTimeCacheValid(src=src, maxTime=maxTime):
            return
        fitCache = self._data[src.item.ID] = {'maxTime': maxTime}
        intCacheRps = fitCache['internalRps'] = {}
        intCacheRepAmount = fitCache['internalRepAmount'] = {}

        def addRps(rrKey, addedTimeStart, addedTimeFinish, addedRepAmounts):
            if not addedRepAmounts:
                return
            repAmountSum = sum(addedRepAmounts, RRTypes(0, 0, 0, 0))
            if repAmountSum.shield > 0 or repAmountSum.armor > 0 or repAmountSum.hull > 0:
                addedRps = repAmountSum / (addedTimeFinish - addedTimeStart)
                rrCacheRps = intCacheRps.setdefault(rrKey, [])
                rrCacheRps.append((addedTimeStart, addedTimeFinish, addedRps))

        def addRepAmount(rrKey, addedTime, addedRepAmount):
            if addedRepAmount.shield > 0 or addedRepAmount.armor > 0 or addedRepAmount.hull > 0:
                intCacheRepAmount.setdefault(rrKey, {})[addedTime] = addedRepAmount

        # Modules
        for mod in src.item.activeModulesIter():
            if not mod.isRemoteRepping():
                continue
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTimeMs, inactiveTimeMs in cycleParams.iterCycles():
                cycleRepAmounts = []
                repAmountParams = mod.getRepAmountParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for repTimeMs, repAmount in repAmountParams.items():
                    cycleRepAmounts.append(repAmount)
                    addRepAmount(mod, currentTime + repTimeMs / 1000, repAmount)
                addRps(mod, currentTime, currentTime + cycleTimeMs / 1000, cycleRepAmounts)
                if inactiveTimeMs > 0:
                    nonstopCycles = 0
                else:
                    nonstopCycles += 1
                if currentTime > maxTime:
                    break
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
        # Drones
        for drone in src.item.activeDronesIter():
            if not drone.isRemoteRepping():
                continue
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            repAmountParams = drone.getRepAmountParameters()
            for cycleTimeMs, inactiveTimeMs in cycleParams.iterCycles():
                cycleRepAmounts = []
                for repTimeMs, repAmount in repAmountParams.items():
                    cycleRepAmounts.append(repAmount)
                    addRepAmount(drone, currentTime + repTimeMs / 1000, repAmount)
                addRps(drone, currentTime, currentTime + cycleTimeMs / 1000, cycleRepAmounts)
                if currentTime > maxTime:
                    break
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000

    def _isTimeCacheValid(self, src, maxTime):
        try:
            cacheMaxTime = self._data[src.item.ID]['maxTime']
        except KeyError:
            return False
        return maxTime <= cacheMaxTime

    def _getDataPoint(self, src, time, dataFunc):
        data = dataFunc(src)
        timesBefore = [t for t in data if floatUnerr(t) <= floatUnerr(time)]
        try:
            time = max(timesBefore)
        except ValueError:
            return {}
        else:
            return data[time]
