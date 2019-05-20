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


from itertools import chain

from eos.graph import Graph
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from gui.utils.numberFormatter import roundToPrec


class FitDpsTimeGraph(Graph):

    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        # We deliberately ignore xAmount here to build graph which will reflect
        # all steps of building up the damage
        minX, maxX = xRange
        if fit.ID not in self.cache:
            self.__generateCache(fit, maxX)
        currentY = None
        xs = []
        ys = []
        cache = self.cache[fit.ID]
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
        cache = self.cache[fit.ID]
        closestTime = max((t for t in cache if t <= time), default=None)
        if closestTime is None:
            return 0
        return roundToPrec(cache[closestTime], 6)

    def __generateCache(self, fit, maxTime):
        cache = []

        def addDmg(addedTimeStart, addedTimeFinish, addedDmg):
            if addedDmg == 0:
                return
            addedDps = 1000 * addedDmg / (addedTimeFinish - addedTimeStart)
            cache.append((addedTimeStart, addedTimeFinish, addedDps))

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
                cycleDamage = 0
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTime, volley in volleyParams.items():
                    cycleDamage += volley.total
                addDmg(currentTime, currentTime + cycleTime, cycleDamage)
                currentTime += cycleTime + inactiveTime
                if inactiveTime > 0:
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
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                cycleDamage = 0
                volleyParams = drone.getVolleyParameters()
                for volleyTime, volley in volleyParams.items():
                    cycleDamage += volley.total
                addDmg(currentTime, currentTime + cycleTime, cycleDamage)
                currentTime += cycleTime + inactiveTime
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
                for cycleTime, inactiveTime in abilityCycleParams.iterCycles():
                    cycleDamage = 0
                    for volleyTime, volley in abilityVolleyParams.items():
                        cycleDamage += volley.total
                    addDmg(currentTime, currentTime + cycleTime, cycleDamage)
                    currentTime += cycleTime + inactiveTime
                    if currentTime > maxTime:
                        break

        # Post-process cache
        finalCache = {}
        for time in sorted(set(chain((i[0] for i in cache), (i[1] for i in cache)))):
            entries = (e for e in cache if e[0] <= time < e[1])
            dps = sum(e[2] for e in entries)
            finalCache[time] = dps
        self.cache[fit.ID] = finalCache
