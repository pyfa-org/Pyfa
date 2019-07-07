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


class FitCapRegenGraph(FitGraph):

    # UI stuff
    internalName = 'capRegenGraph'
    name = 'Capacitor Regeneration'
    xDefs = [
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
        XDef(handle='capAmount', unit='GJ', label='Cap amount', mainInput=('capAmount', '%')),
        XDef(handle='capAmount', unit='%', label='Cap amount', mainInput=('capAmount', '%'))]
    yDefs = [
        YDef(handle='capAmount', unit='GJ', label='Cap amount'),
        YDef(handle='capRegen', unit='GJ/s', label='Cap regen')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=120, defaultRange=(0, 300), mainOnly=True),
        Input(handle='capAmount', unit='%', label='Cap amount', iconID=1668, defaultValue=25, defaultRange=(0, 100), mainOnly=True)]
    srcExtraCols = ('CapAmount', 'CapTime')

    # Calculation stuff
    _normalizers = {
        ('capAmount', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('capacitorCapacity')}
    _limiters = {
        'capAmount': lambda fit, tgt: (0, fit.ship.getModifiedItemAttr('capacitorCapacity'))}
    _denormalizers = {
        ('capAmount', '%'): lambda v, fit, tgt: v * 100 / fit.ship.getModifiedItemAttr('capacitorCapacity')}

    def _time2capAmount(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxCapAmount = fit.ship.getModifiedItemAttr('capacitorCapacity')
        capRegenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        for time in self._iterLinear(mainInput[1]):
            currentCapAmount = calculateCapAmount(maxCapAmount=maxCapAmount, capRegenTime=capRegenTime, time=time)
            xs.append(time)
            ys.append(currentCapAmount)
        return xs, ys

    def _time2capRegen(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxCapAmount = fit.ship.getModifiedItemAttr('capacitorCapacity')
        capRegenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        for time in self._iterLinear(mainInput[1]):
            currentCapAmount = calculateCapAmount(maxCapAmount=maxCapAmount, capRegenTime=capRegenTime, time=time)
            currentCapRegen = calculateCapRegen(maxCapAmount=maxCapAmount, capRegenTime=capRegenTime, currentCapAmount=currentCapAmount)
            xs.append(time)
            ys.append(currentCapRegen)
        return xs, ys

    def _capAmount2capAmount(self, mainInput, miscInputs, fit, tgt):
        # Useless, but valid combination of x and y
        xs = []
        ys = []
        for currentCapAmount in self._iterLinear(mainInput[1]):
            xs.append(currentCapAmount)
            ys.append(currentCapAmount)
        return xs, ys

    def _capAmount2capRegen(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxCapAmount = fit.ship.getModifiedItemAttr('capacitorCapacity')
        capRegenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        for currentCapAmount in self._iterLinear(mainInput[1]):
            currentCapRegen = calculateCapRegen(maxCapAmount=maxCapAmount, capRegenTime=capRegenTime, currentCapAmount=currentCapAmount)
            xs.append(currentCapAmount)
            ys.append(currentCapRegen)
        return xs, ys

    _getters = {
        ('time', 'capAmount'): _time2capAmount,
        ('time', 'capRegen'): _time2capRegen,
        ('capAmount', 'capAmount'): _capAmount2capAmount,
        ('capAmount', 'capRegen'): _capAmount2capRegen}


def calculateCapAmount(maxCapAmount, capRegenTime, time):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return maxCapAmount * (1 + math.exp(5 * -time / capRegenTime) * -1) ** 2


def calculateCapRegen(maxCapAmount, capRegenTime, currentCapAmount):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return 10 * maxCapAmount / capRegenTime * (math.sqrt(currentCapAmount / maxCapAmount) - currentCapAmount / maxCapAmount)


FitCapRegenGraph.register()
