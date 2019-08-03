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


class Time2CapAmountGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxCapAmount': src.item.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': src.item.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        capAmount = calculateCapAmount(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            time=time)
        return capAmount


class Time2CapRegenGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxCapAmount': src.item.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': src.item.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        capAmount = calculateCapAmount(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            time=time)
        capRegen = calculateCapRegen(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            currentCapAmount=capAmount)
        return capRegen


# Useless, but valid combination of x and y
class CapAmount2CapAmountGetter(SmoothPointGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        capAmount = x
        return capAmount


class CapAmount2CapRegenGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxCapAmount': src.item.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': src.item.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        capAmount = x
        capRegen = calculateCapRegen(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            currentCapAmount=capAmount)
        return capRegen


def calculateCapAmount(maxCapAmount, capRegenTime, time):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return maxCapAmount * (1 + math.exp(5 * -time / capRegenTime) * -1) ** 2


def calculateCapRegen(maxCapAmount, capRegenTime, currentCapAmount):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return 10 * maxCapAmount / capRegenTime * (math.sqrt(currentCapAmount / maxCapAmount) - currentCapAmount / maxCapAmount)
