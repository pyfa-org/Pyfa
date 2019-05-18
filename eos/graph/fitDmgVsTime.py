# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================


from eos.graph import Graph
from eos.utils.spoolSupport import SpoolType, SpoolOptions


class FitDmgVsTimeGraph(Graph):

    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        # We deliberately ignore xAmount here to build graph which will reflect
        # all steps of building up the damage
        maxTime = xRange[1]
        if fit.ID not in self.cache:
            self.__generateCache(fit, maxTime)
        currentY = 0
        # Add zeros even if there's some damage dealt at time = 0, to explicitly show that
        # volley is done at this time
        xs = [0]
        ys = [0]
        cache = self.cache[fit.ID]
        for time in sorted(cache):
            prevY = currentY
            currentX = time / 1000
            currentY = cache[time]
            if currentY != prevY:
                xs.append(currentX)
                ys.append(prevY)
                xs.append(currentX)
                ys.append(currentY)
        if maxTime > max(xs):
            xs.append(maxTime)
            ys.append(ys[-1])
        return xs, ys

    def getYForX(self, fit, extraData, x):
        time = x * 1000
        cache = self.cache[fit.ID]
        closestTime = max((t for t in cache if t <= time), default=None)
        if closestTime is None:
            return 0
        return cache[closestTime]

    def __generateCache(self, fit, maxTime):
        cache = self.cache[fit.ID] = {}

        def addDmg(addedTime, addedDmg):
            if addedDmg == 0:
                return
            if addedTime not in cache:
                prevTime = max((t for t in cache if t < addedTime), default=None)
                if prevTime is None:
                    cache[addedTime] = 0
                else:
                    cache[addedTime] = cache[prevTime]
            for time in (t for t in cache if t >= addedTime):
                cache[time] += addedDmg

        # We'll handle calculations in milliseconds
        maxTime = maxTime * 1000
        for mod in fit.modules:
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTime, volley in volleyParams.items():
                    if currentTime + volleyTime <= maxTime and volleyTime <= cycleTime:
                        addDmg(currentTime + volleyTime, volley.total)
                currentTime += cycleTime
                currentTime += inactiveTime
                if inactiveTime == 0:
                    nonstopCycles += 1
                else:
                    nonstopCycles = 0
                if currentTime > maxTime:
                    break
        for drone in fit.drones:
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            volleyParams = drone.getVolleyParameters()
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                for volleyTime, volley in volleyParams.items():
                    if currentTime + volleyTime <= maxTime and volleyTime <= cycleTime:
                        addDmg(currentTime + volleyTime, volley.total)
                currentTime += cycleTime
                currentTime += inactiveTime
                if currentTime > maxTime:
                    break
        for fighter in fit.fighters:
            cycleParams = fighter.getCycleParametersPerEffectOptimizedDps(reloadOverride=True)
            if cycleParams is None:
                continue
            volleyParams = fighter.getVolleyParametersPerEffect()
            for effectID, abilityCycleParams in cycleParams.items():
                if effectID not in volleyParams:
                    continue
                currentTime = 0
                abilityVolleyParams = volleyParams[effectID]
                for cycleTime, inactiveTime in abilityCycleParams.iterCycles():
                    for volleyTime, volley in abilityVolleyParams.items():
                        if currentTime + volleyTime <= maxTime and volleyTime <= cycleTime:
                            addDmg(currentTime + volleyTime, volley.total)
                    currentTime += cycleTime
                    currentTime += inactiveTime
                    if currentTime > maxTime:
                        break
