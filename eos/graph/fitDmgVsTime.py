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
from gui.utils.numberFormatter import roundToPrec


class FitDmgVsTimeGraph(Graph):

    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        # We deliberately ignore xAmount here to build graph which will reflect
        # all steps of building up the damage
        minX, maxX = self._limitXRange(xRange, fit, extraData)
        if fit.ID not in self._cache:
            self.__generateCache(fit, maxX)
        currentY = None
        xs = []
        ys = []
        cache = self._cache[fit.ID]
        for time in sorted(cache):
            prevY = currentY
            currentX = time / 1000
            currentY = roundToPrec(cache[time], 6)
            if currentX < minX:
                continue
            # First set of data points
            if not xs:
                # Start at exactly requested time, at last known value
                initialY = prevY or 0
                xs.append(minX)
                ys.append(initialY)
                # If current time is bigger then starting, extend plot to that time with old value
                if currentX > minX:
                    xs.append(currentX)
                    ys.append(initialY)
                # If new value is different, extend it with new point to the new value
                if currentY != prevY:
                    xs.append(currentX)
                    ys.append(currentY)
                continue
            # Last data point
            if currentX > maxX:
                xs.append(maxX)
                ys.append(prevY)
                break
            # Anything in-between
            if currentY != prevY:
                if prevY is not None:
                    xs.append(currentX)
                    ys.append(prevY)
                xs.append(currentX)
                ys.append(currentY)
            if currentX >= maxX:
                break
        return xs, ys

    def getYForX(self, fit, extraData, x):
        time = x * 1000
        cache = self._cache[fit.ID]
        closestTime = max((t for t in cache if t <= time), default=None)
        if closestTime is None:
            return 0
        return roundToPrec(cache[closestTime], 6)

    def _getXLimits(self, fit, extraData):
        return 0, 1000

    def __generateCache(self, fit, maxTime):
        cache = self._cache[fit.ID] = {}

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
            if not mod.isDealingDamage():
                continue
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTime, volley in volleyParams.items():
                    addDmg(currentTime + volleyTime, volley.total)
                if inactiveTime == 0:
                    nonstopCycles += 1
                else:
                    nonstopCycles = 0
                if currentTime > maxTime:
                    break
                currentTime += cycleTime + inactiveTime
        for drone in fit.drones:
            if not drone.isDealingDamage():
                continue
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            volleyParams = drone.getVolleyParameters()
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                for volleyTime, volley in volleyParams.items():
                    addDmg(currentTime + volleyTime, volley.total)
                if currentTime > maxTime:
                    break
                currentTime += cycleTime + inactiveTime
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
                for cycleTime, inactiveTime in abilityCycleParams.iterCycles():
                    for volleyTime, volley in abilityVolleyParams.items():
                        addDmg(currentTime + volleyTime, volley.total)
                    if currentTime > maxTime:
                        break
                    currentTime += cycleTime + inactiveTime
