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


class FitDpsTimeGraph(Graph):

    defaults = {"time": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcDps, data if data is not None else self.defaults)
        self.fit = fit
        self.__cache = []

    def calcDps(self, data):
        time = data["time"] * 1000
        entries = (e for e in self.__cache if e[0] <= time < e[1])
        dps = sum(e[2] for e in entries)
        return dps

    def recalc(self):

        def addDmg(addedTimeStart, addedTimeFinish, addedDmg):
            if addedDmg == 0:
                return
            addedDps = 1000 * addedDmg / (addedTimeFinish - addedTimeStart)
            self.__cache.append((addedTimeStart, addedTimeFinish, addedDps))

        self.__cache = []
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
                cycleDamage = 0
                volleyParams = mod.getVolleyParameters(spoolOptions=SpoolOptions(SpoolType.CYCLES, nonstopCycles, True))
                for volleyTime, volley in volleyParams.items():
                    if currentTime + volleyTime <= maxTime and volleyTime <= cycleTime:
                        cycleDamage += volley.total
                addDmg(currentTime, currentTime + cycleTime, cycleDamage)
                currentTime += cycleTime
                currentTime += inactiveTime
                if inactiveTime > 0:
                    nonstopCycles = 0
                else:
                    nonstopCycles += 1
                if currentTime > maxTime:
                    break
        for drone in fit.drones:
            cycleParams = drone.getCycleParameters(reloadOverride=True)
            if cycleParams is None:
                continue
            currentTime = 0
            for cycleTime, inactiveTime in cycleParams.iterCycles():
                cycleDamage = 0
                volleyParams = drone.getVolleyParameters()
                for volleyTime, volley in volleyParams.items():
                    if currentTime + volleyTime <= maxTime and volleyTime <= cycleTime:
                        cycleDamage += volley.total
                addDmg(currentTime, currentTime + cycleTime, cycleDamage)
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
                abilityVolleyParams = volleyParams[effectID]
                currentTime = 0
                for cycleTime, inactiveTime in abilityCycleParams.iterCycles():
                    cycleDamage = 0
                    for volleyTime, volley in abilityVolleyParams.items():
                        if currentTime + volleyTime <= maxTime and volleyTime <= cycleTime:
                            cycleDamage += volley.total
                    addDmg(currentTime, currentTime + cycleTime, cycleDamage)
                    currentTime += cycleTime
                    currentTime += inactiveTime
                    if currentTime > maxTime:
                        break
