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


class FitShieldRegenGraph(FitGraph):

    # UI stuff
    internalName = 'shieldRegenGraph'
    name = 'Shield Regeneration'
    xDefs = [
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
        XDef(handle='shieldAmount', unit='EHP', label='Shield amount', mainInput=('shieldAmount', '%')),
        XDef(handle='shieldAmount', unit='HP', label='Shield amount', mainInput=('shieldAmount', '%')),
        XDef(handle='shieldAmount', unit='%', label='Shield amount', mainInput=('shieldAmount', '%'))]
    yDefs = [
        YDef(handle='shieldAmount', unit='EHP', label='Shield amount'),
        YDef(handle='shieldAmount', unit='HP', label='Shield amount'),
        YDef(handle='shieldRegen', unit='EHP/s', label='Shield regen'),
        YDef(handle='shieldRegen', unit='HP/s', label='Shield regen')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=120, defaultRange=(0, 300), mainOnly=True),
        Input(handle='shieldAmount', unit='%', label='Shield amount', iconID=1384, defaultValue=25, defaultRange=(0, 100), mainOnly=True)]
    srcExtraCols = ('ShieldAmount', 'ShieldTime')

    # Calculation stuff
    _normalizers = {
        ('shieldAmount', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('shieldCapacity')}
    _limiters = {
        'shieldAmount': lambda fit, tgt: (0, fit.ship.getModifiedItemAttr('shieldCapacity'))}
    _denormalizers = {
        ('shieldAmount', '%'): lambda v, fit, tgt: v * 100 / fit.ship.getModifiedItemAttr('shieldCapacity'),
        ('shieldAmount', 'EHP'): lambda v, fit, tgt: fit.damagePattern.effectivify(fit, v, 'shield'),
        ('shieldRegen', 'EHP/s'): lambda v, fit, tgt: fit.damagePattern.effectivify(fit, v, 'shield')}

    def _time2shieldAmount(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxShieldAmount = fit.ship.getModifiedItemAttr('shieldCapacity')
        shieldRegenTime = fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        for time in self._iterLinear(mainInput[1]):
            currentShieldAmount = calculateShieldAmount(maxShieldAmount=maxShieldAmount, shieldRegenTime=shieldRegenTime, time=time)
            xs.append(time)
            ys.append(currentShieldAmount)
        return xs, ys

    def _time2shieldRegen(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxShieldAmount = fit.ship.getModifiedItemAttr('shieldCapacity')
        shieldRegenTime = fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        for time in self._iterLinear(mainInput[1]):
            currentShieldAmount = calculateShieldAmount(maxShieldAmount=maxShieldAmount, shieldRegenTime=shieldRegenTime, time=time)
            currentShieldRegen = calculateShieldRegen(maxShieldAmount=maxShieldAmount, shieldRegenTime=shieldRegenTime, currentShieldAmount=currentShieldAmount)
            xs.append(time)
            ys.append(currentShieldRegen)
        return xs, ys

    def _shieldAmount2shieldAmount(self, mainInput, miscInputs, fit, tgt):
        # Useless, but valid combination of x and y
        xs = []
        ys = []
        for currentShieldAmount in self._iterLinear(mainInput[1]):
            xs.append(currentShieldAmount)
            ys.append(currentShieldAmount)
        return xs, ys

    def _shieldAmount2shieldRegen(self, mainInput, miscInputs, fit, tgt):
        xs = []
        ys = []
        maxShieldAmount = fit.ship.getModifiedItemAttr('shieldCapacity')
        shieldRegenTime = fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        for currentShieldAmount in self._iterLinear(mainInput[1]):
            currentShieldRegen = calculateShieldRegen(maxShieldAmount=maxShieldAmount, shieldRegenTime=shieldRegenTime, currentShieldAmount=currentShieldAmount)
            xs.append(currentShieldAmount)
            ys.append(currentShieldRegen)
        return xs, ys

    _getters = {
        ('time', 'shieldAmount'): _time2shieldAmount,
        ('time', 'shieldRegen'): _time2shieldRegen,
        ('shieldAmount', 'shieldAmount'): _shieldAmount2shieldAmount,
        ('shieldAmount', 'shieldRegen'): _shieldAmount2shieldRegen}


def calculateShieldAmount(maxShieldAmount, shieldRegenTime, time):
    # The same formula as for cap
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return maxShieldAmount * (1 + math.exp(5 * -time / shieldRegenTime) * -1) ** 2


def calculateShieldRegen(maxShieldAmount, shieldRegenTime, currentShieldAmount):
    # The same formula as for cap
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return 10 * maxShieldAmount / shieldRegenTime * (math.sqrt(currentShieldAmount / maxShieldAmount) - currentShieldAmount / maxShieldAmount)


FitShieldRegenGraph.register()
