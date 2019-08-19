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

from graphs.data.base import SmoothPointGetter


class Time2ShieldAmountGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxShieldAmount': src.item.ship.getModifiedItemAttr('shieldCapacity'),
            'shieldRegenTime': src.item.ship.getModifiedItemAttr('shieldRechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        shieldAmount = calculateShieldAmount(
            maxShieldAmount=commonData['maxShieldAmount'],
            shieldRegenTime=commonData['shieldRegenTime'],
            shieldAmountT0=miscParams['shieldAmountT0'] or 0,
            time=time)
        return shieldAmount


class Time2ShieldRegenGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxShieldAmount': src.item.ship.getModifiedItemAttr('shieldCapacity'),
            'shieldRegenTime': src.item.ship.getModifiedItemAttr('shieldRechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        shieldAmount = calculateShieldAmount(
            maxShieldAmount=commonData['maxShieldAmount'],
            shieldRegenTime=commonData['shieldRegenTime'],
            shieldAmountT0=miscParams['shieldAmountT0'] or 0,
            time=time)
        shieldRegen = calculateShieldRegen(
            maxShieldAmount=commonData['maxShieldAmount'],
            shieldRegenTime=commonData['shieldRegenTime'],
            currentShieldAmount=shieldAmount)
        return shieldRegen


# Useless, but valid combination of x and y
class ShieldAmount2ShieldAmountGetter(SmoothPointGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        shieldAmount = x
        return shieldAmount


class ShieldAmount2ShieldRegenGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxShieldAmount': src.item.ship.getModifiedItemAttr('shieldCapacity'),
            'shieldRegenTime': src.item.ship.getModifiedItemAttr('shieldRechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        shieldAmount = x
        shieldRegen = calculateShieldRegen(
            maxShieldAmount=commonData['maxShieldAmount'],
            shieldRegenTime=commonData['shieldRegenTime'],
            currentShieldAmount=shieldAmount)
        return shieldRegen


def calculateShieldAmount(maxShieldAmount, shieldRegenTime, shieldAmountT0, time):
    # The same formula as for cap
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return maxShieldAmount * (1 + math.exp(5 * -time / shieldRegenTime) * (math.sqrt(shieldAmountT0 / maxShieldAmount) - 1)) ** 2


def calculateShieldRegen(maxShieldAmount, shieldRegenTime, currentShieldAmount):
    # The same formula as for cap
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return 10 * maxShieldAmount / shieldRegenTime * (math.sqrt(currentShieldAmount / maxShieldAmount) - currentShieldAmount / maxShieldAmount)
