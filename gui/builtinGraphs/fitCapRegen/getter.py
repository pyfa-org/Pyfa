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

from gui.builtinGraphs.base import SmoothPointGetter


class Time2CapAmountGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, fit, tgt):
        return {
            'maxCapAmount': fit.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': fit.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        y = calculateCapAmount(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            time=x)
        return y


class Time2CapRegenGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, fit, tgt):
        return {
            'maxCapAmount': fit.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': fit.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        currentCapAmount = calculateCapAmount(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            time=x)
        y = calculateCapRegen(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            currentCapAmount=currentCapAmount)
        return y


# Useless, but valid combination of x and y
class CapAmount2CapAmountGetter(SmoothPointGetter):

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        return x


class CapAmount2CapRegenGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, fit, tgt):
        return {
            'maxCapAmount': fit.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': fit.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        y = calculateCapRegen(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            currentCapAmount=x)
        return y


def calculateCapAmount(maxCapAmount, capRegenTime, time):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return maxCapAmount * (1 + math.exp(5 * -time / capRegenTime) * -1) ** 2


def calculateCapRegen(maxCapAmount, capRegenTime, currentCapAmount):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return 10 * maxCapAmount / capRegenTime * (math.sqrt(currentCapAmount / maxCapAmount) - currentCapAmount / maxCapAmount)
