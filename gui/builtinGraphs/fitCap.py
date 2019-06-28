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


class FitCapAmountVsTimeGraph(FitGraph):

    name = 'Capacitor'

    # UI stuff
    @property
    def xDefs(self):
        return [XDef(handle='time', unit='s', label='Time', mainInput=('time', 's'))]

    @property
    def yDefs(self):
        return [YDef(handle='capAmount', unit='GJ', label='Cap amount')]

    @property
    def inputs(self):
        return [Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=120, defaultRange=(0, 300), mainOnly=False)]

    # Calculation stuff
    def _time2capAmount(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxCap = fit.ship.getModifiedItemAttr('capacitorCapacity')
        regenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        for time in self._iterLinear(mainInput[1]):
            # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
            cap = maxCap * (1 + math.exp(5 * -time / regenTime) * -1) ** 2
            xs.append(time)
            ys.append(cap)
        return xs, ys

    _getters = {
        ('time', 'capAmount'): _time2capAmount}


FitCapAmountVsTimeGraph.register()
