# ===============================================================================
# Copyright (C) 2010 Diego Duclos, 2017 taleden
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

from math import sin, radians

from eos.graph import Graph
from logbook import Logger

pyfalog = Logger(__name__)


class FitDpsGraph(Graph):
    defaults = {
        "emRes"          : 0,
        "thRes"          : 0,
        "kiRes"          : 0,
        "exRes"          : 0,
        "distance"       : 0,
        "signatureRadius": 0,
        "atkAngle"       : 0,
        "atkSpeed"       : 0,
        "tgtAngle"       : 0,
        "tgtSpeed"       : 0,
    }

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcDps, data if data is not None else self.defaults)
        self.fit = fit

    def calcDps(self, data):
        fit = self.fit

        distance = (data["distance"] or 0) * 1000
        signatureRadius = (data["signatureRadius"] or 0) * fit.calculateTargetSignatureRadiusMultiplier(distance)
        tgtSpeed = (data["tgtSpeed"] or 0) * fit.calculateTargetSpeedModifier(distance)
        transversal = sin(radians(data["atkAngle"])) * data["atkSpeed"] + sin(radians(data["tgtAngle"])) * tgtSpeed

        total = 0

        for mod,count in fit.weaponModules:
            dps, _ = mod.damageStats(data["emRes"]/100.0, data["thRes"]/100.0, data["kiRes"]/100.0, data["exRes"]/100.0, distance, signatureRadius, tgtSpeed, transversal)
            total += dps * count

        if distance <= fit.extraAttributes["droneControlRange"]:
            for drone in fit.drones:
                dps, _ = drone.damageStats(data["emRes"]/100.0, data["thRes"]/100.0, data["kiRes"]/100.0, data["exRes"]/100.0, distance, signatureRadius, tgtSpeed, transversal)
                total += dps

        for fighter in fit.fighters:
            dps, _ = fighter.damageStats(data["emRes"]/100.0, data["thRes"]/100.0, data["kiRes"]/100.0, data["exRes"]/100.0, distance, signatureRadius, tgtSpeed, transversal)
            total += dps * multiplier

        return total
