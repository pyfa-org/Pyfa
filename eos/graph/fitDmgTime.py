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

from logbook import Logger

from eos.graph import Graph
from eos.utils.spoolSupport import SpoolType, SpoolOptions


pyfalog = Logger(__name__)


class FitDmgTimeGraph(Graph):

    defaults = {"time": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcDmg, data if data is not None else self.defaults)
        self.fit = fit
        self.__cache = {}

    def calcDmg(self, data):
        time = data["time"] * 1000
        closestTime = max((t for t in self.__cache if t <= time), default=None)
        if closestTime is None:
            return 0
        return self.__cache[closestTime]

    def recalc(self):

        def addDmg(addedTime, addedDmg):
            if addDmg == 0:
                return
            if addedTime not in self.__cache:
                prevTime = max((t for t in self.__cache if t < addedTime), default=None)
                if prevTime is None:
                    self.__cache[addedTime] = 0
                else:
                    self.__cache[addedTime] = self.__cache[prevTime]
            for time in (t for t in self.__cache if t >= addedTime):
                self.__cache[time] += addedDmg

        self.__cache.clear()
        fit = self.fit
        # We'll handle calculations in milliseconds
        maxTime = self.data["time"].data[0].end * 1000
        for mod in fit.modules:
            cycleParams = mod.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            nonstopCycles = 0
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTime, volley in volleyParams.items():
                    if currentTime + volleyTime <= maxTime:
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
                    if currentTime + volleyTime <= maxTime:
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
                        if currentTime + volleyTime <= maxTime:
                            addDmg(currentTime + volleyTime, volley.total)
                    currentTime += cycleTime
                    currentTime += inactiveTime
                    if currentTime > maxTime:
                        break
