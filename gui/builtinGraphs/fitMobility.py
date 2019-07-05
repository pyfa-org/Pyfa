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


import math

from .base import FitGraph, XDef, YDef, Input


class FitMobilityVsTimeGraph(FitGraph):

    # UI stuff
    internalName = 'mobilityGraph'
    name = 'Mobility'
    xDefs = [
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's'))]
    yDefs = [
        YDef(handle='speed', unit='m/s', label='Speed'),
        YDef(handle='distance', unit='km', label='Distance')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=10, defaultRange=(0, 30), mainOnly=False)]

    # Calculation stuff
    _denormalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v / 1000}

    def _time2speed(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        mass = fit.ship.getModifiedItemAttr('mass')
        agility = fit.ship.getModifiedItemAttr('agility')
        for time in self._iterLinear(mainInput[1]):
            # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
            speed = maxSpeed * (1 - math.exp((-time * 1000000) / (agility * mass)))
            xs.append(time)
            ys.append(speed)
        return xs, ys

    def _time2distance(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        mass = fit.ship.getModifiedItemAttr('mass')
        agility = fit.ship.getModifiedItemAttr('agility')
        for time in self._iterLinear(mainInput[1]):
            # Definite integral of:
            # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
            distance_t = maxSpeed * time + (maxSpeed * agility * mass * math.exp((-time * 1000000) / (agility * mass)) / 1000000)
            distance_0 = maxSpeed * 0 + (maxSpeed * agility * mass * math.exp((-0 * 1000000) / (agility * mass)) / 1000000)
            distance = distance_t - distance_0
            xs.append(time)
            ys.append(distance)
        return xs, ys

    _getters = {
        ('time', 'speed'): _time2speed,
        ('time', 'distance'): _time2distance}


FitMobilityVsTimeGraph.register()
