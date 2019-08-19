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
from eos.utils.stats import DmgTypes
from graphs.data.base import FitDataCache


class TimeCache(FitDataCache):

    # Whole data getters
    def getDpsData(self, src):
        """Return DPS data in {time: {key: dps}} format."""
        return self._data[src.item.ID]['finalDps']

    def getVolleyData(self, src):
        """Return volley data in {time: {key: volley}} format."""
        return self._data[src.item.ID]['finalVolley']

    def getDmgData(self, src):
        """Return inflicted damage data in {time: {key: damage}} format."""
        return self._data[src.item.ID]['finalDmg']

    # Specific data point getters
    def getDpsDataPoint(self, src, time):
        """Get DPS data by specified time in {key: dps} format."""
        return self._getDataPoint(src=src, time=time, dataFunc=self.getDpsData)

    def getVolleyDataPoint(self, src, time):
        """Get volley data by specified time in {key: volley} format."""
        return self._getDataPoint(src=src, time=time, dataFunc=self.getVolleyData)

    def getDmgDataPoint(self, src, time):
        """Get inflicted damage data by specified time in {key: dmg} format."""
        return self._getDataPoint(src=src, time=time, dataFunc=self.getDmgData)

    # Preparation functions
    def prepareDpsData(self, src, maxTime):
        self._prepareDpsVolleyData(src=src, maxTime=maxTime)

    def prepareVolleyData(self, src, maxTime):
        self._prepareDpsVolleyData(src=src, maxTime=maxTime)

    def prepareDmgData(self, src, maxTime):
        # Time is none means that time parameter has to be ignored,
        # we do not need cache for that
        if maxTime is None:
            return
        self._generateInternalForm(src=src, maxTime=maxTime)
        fitCache = self._data[src.item.ID]
        # Final cache has been generated already, don't do anything
        if 'finalDmg' in fitCache:
            return
        intCache = fitCache['internalDmg']
        changesByTime = {}
        for key, dmgMap in intCache.items():
            for time in dmgMap:
                changesByTime.setdefault(time, []).append(key)
        # Here we convert cache to following format:
        # {time: {key: damage done by key at this time}}
        finalCache = fitCache['finalDmg'] = {}
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
        # We do not need internal cache once we have final
        del fitCache['internalDmg']

    # Private stuff
    def _prepareDpsVolleyData(self, src, maxTime):
        # Time is none means that time parameter has to be ignored,
        # we do not need cache for that
        if maxTime is None:
            return True
        self._generateInternalForm(src=src, maxTime=maxTime)
        fitCache = self._data[src.item.ID]
        # Final cache has been generated already, don't do anything
        if 'finalDps' in fitCache and 'finalVolley' in fitCache:
            return
        # Convert cache from segments with assigned values into points
        # which are located at times when dps/volley values change
        pointCache = {}
        for key, dmgList in fitCache['internalDpsVolley'].items():
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
        # We have data in another form, do not need old one any longer
        del fitCache['internalDpsVolley']
        changesByTime = {}
        for key, dmgMap in pointCache.items():
            for time in dmgMap:
                changesByTime.setdefault(time, []).append(key)
        # Here we convert cache to following format:
        # {time: {key: (dps, volley}}
        finalDpsCache = fitCache['finalDps'] = {}
        finalVolleyCache = fitCache['finalVolley'] = {}
        timeDpsData = {}
        timeVolleyData = {}
        for time in sorted(changesByTime):
            timeDpsData = copy(timeDpsData)
            timeVolleyData = copy(timeVolleyData)
            for key in changesByTime[time]:
                dps, volley = pointCache[key][time]
                timeDpsData[key] = dps
                timeVolleyData[key] = volley
            finalDpsCache[time] = timeDpsData
            finalVolleyCache[time] = timeVolleyData

    def _generateInternalForm(self, src, maxTime):
        if self._isTimeCacheValid(src=src, maxTime=maxTime):
            return
        fitCache = self._data[src.item.ID] = {'maxTime': maxTime}
        intCacheDpsVolley = fitCache['internalDpsVolley'] = {}
        intCacheDmg = fitCache['internalDmg'] = {}

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
        for mod in src.item.activeModulesIter():
            if not mod.isDealingDamage():
                continue
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTimeMs, inactiveTimeMs, isInactivityReload in cycleParams.iterCycles():
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
        for drone in src.item.activeDronesIter():
            if not drone.isDealingDamage():
                continue
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            volleyParams = drone.getVolleyParameters()
            for cycleTimeMs, inactiveTimeMs, isInactivityReload in cycleParams.iterCycles():
                cycleVolleys = []
                for volleyTimeMs, volley in volleyParams.items():
                    cycleVolleys.append(volley)
                    addDmg(drone, currentTime + volleyTimeMs / 1000, volley)
                addDpsVolley(drone, currentTime, currentTime + cycleTimeMs / 1000, cycleVolleys)
                if currentTime > maxTime:
                    break
                currentTime += cycleTimeMs / 1000 + inactiveTimeMs / 1000
        # Fighters
        for fighter in src.item.activeFightersIter():
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
                for cycleTimeMs, inactiveTimeMs, isInactivityReload in abilityCycleParams.iterCycles():
                    cycleVolleys = []
                    for volleyTimeMs, volley in abilityVolleyParams.items():
                        cycleVolleys.append(volley)
                        addDmg((fighter, effectID), currentTime + volleyTimeMs / 1000, volley)
                    addDpsVolley((fighter, effectID), currentTime, currentTime + cycleTimeMs / 1000, cycleVolleys)
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
