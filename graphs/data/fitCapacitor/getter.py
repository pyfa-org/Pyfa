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

    def getRange(self, xRange, miscParams, src, tgt):
        # Use smooth getter when we're not using cap sim
        if not miscParams['useCapsim']:
            return super().getRange(xRange=xRange, miscParams=miscParams, src=src, tgt=tgt)
        capAmountT0 = miscParams['capAmountT0'] or 0
        capSimDataRaw = src.item.getCapSimData(startingCap=capAmountT0)
        # Same here, no cap sim data - use smooth getter which considers only regen
        if not capSimDataRaw:
            return super().getRange(xRange=xRange, miscParams=miscParams, src=src, tgt=tgt)
        capSimDataMaxTime = capSimDataRaw[-1][0]
        minTime, maxTime = xRange
        maxTime = min(maxTime, capSimDataMaxTime)
        maxPointXDistance = (maxTime - minTime) / self._baseResolution
        capSimDataInRange = {k: v for k, v in capSimDataRaw if minTime <= k <= maxTime}
        prevTime = minTime
        xs = []
        ys = []
        capSimDataBefore = {k: v for k, v in capSimDataRaw if k < minTime}
        # When time range lies to the right of last cap sim data point, return nothing
        if len(capSimDataBefore) > 0 and max(capSimDataBefore) == capSimDataMaxTime:
            return xs, ys
        maxCapAmount = src.item.ship.getModifiedItemAttr('capacitorCapacity')
        capRegenTime = src.item.ship.getModifiedItemAttr('rechargeRate') / 1000

        def plotCapRegen(prevTime, prevCap, currentTime):
            subrangeAmount = math.ceil((currentTime - prevTime) / maxPointXDistance)
            subrangeLength = (currentTime - prevTime) / subrangeAmount
            for i in range(1, subrangeAmount + 1):
                subrangeTime = prevTime + subrangeLength * i
                subrangeCap = calculateCapAmount(
                    maxCapAmount=maxCapAmount,
                    capRegenTime=capRegenTime,
                    capAmountT0=prevCap,
                    time=subrangeTime - prevTime)
                xs.append(subrangeTime)
                ys.append(subrangeCap)

        # Calculate starting cap for first value seen in our range
        if capSimDataBefore:
            timeBefore = max(capSimDataBefore)
            capBefore = capSimDataBefore[timeBefore]
            prevCap = calculateCapAmount(
                    maxCapAmount=maxCapAmount,
                    capRegenTime=capRegenTime,
                    capAmountT0=capBefore,
                    time=prevTime - timeBefore)
        else:
            prevCap = calculateCapAmount(
                maxCapAmount=maxCapAmount,
                capRegenTime=capRegenTime,
                capAmountT0=capAmountT0,
                time=prevTime)
        xs.append(prevTime)
        ys.append(prevCap)
        for currentTime in sorted(capSimDataInRange):
            if currentTime > prevTime:
                plotCapRegen(prevTime=prevTime, prevCap=prevCap, currentTime=currentTime)
            currentCap = capSimDataInRange[currentTime]
            xs.append(currentTime)
            ys.append(currentCap)
            prevTime = currentTime
            prevCap = currentCap
        if maxTime > prevTime:
            plotCapRegen(prevTime=prevTime, prevCap=prevCap, currentTime=maxTime)
        return xs, ys

    def getPoint(self, x, miscParams, src, tgt):
        # Use smooth getter when we're not using cap sim
        if not miscParams['useCapsim']:
            return super().getPoint(x=x, miscParams=miscParams, src=src, tgt=tgt)
        capAmountT0 = miscParams['capAmountT0'] or 0
        capSimDataRaw = src.item.getCapSimData(startingCap=capAmountT0)
        # Same here, no cap sim data - use smooth getter which considers only regen
        if not capSimDataRaw:
            return super().getPoint(x=x, miscParams=miscParams, src=src, tgt=tgt)
        currentTime = x
        capSimDataBefore = {k: v for k, v in capSimDataRaw if k <= currentTime}
        capSimDataMaxTime = capSimDataRaw[-1][0]
        # When time range lies to the right of last cap sim data point, return nothing
        if len(capSimDataBefore) > 0 and max(capSimDataBefore) == capSimDataMaxTime:
            return None
        maxCapAmount = src.item.ship.getModifiedItemAttr('capacitorCapacity')
        capRegenTime = src.item.ship.getModifiedItemAttr('rechargeRate') / 1000
        if capSimDataBefore:
            timeBefore = max(capSimDataBefore)
            capBefore = capSimDataBefore[timeBefore]
            if timeBefore == currentTime:
                currentCap = capBefore
            else:
                currentCap = calculateCapAmount(
                        maxCapAmount=maxCapAmount,
                        capRegenTime=capRegenTime,
                        capAmountT0=capBefore,
                        time=currentTime - timeBefore)
        else:
            currentCap = calculateCapAmount(
                maxCapAmount=maxCapAmount,
                capRegenTime=capRegenTime,
                capAmountT0=capAmountT0,
                time=currentTime)
        return currentCap

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxCapAmount': src.item.ship.getModifiedItemAttr('capacitorCapacity'),
            'capRegenTime': src.item.ship.getModifiedItemAttr('rechargeRate') / 1000}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        capAmount = calculateCapAmount(
            maxCapAmount=commonData['maxCapAmount'],
            capRegenTime=commonData['capRegenTime'],
            capAmountT0=miscParams['capAmountT0'] or 0,
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
            capAmountT0=miscParams['capAmountT0'] or 0,
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


def calculateCapAmount(maxCapAmount, capRegenTime, capAmountT0, time):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return maxCapAmount * (1 + math.exp(5 * -time / capRegenTime) * (math.sqrt(capAmountT0 / maxCapAmount) - 1)) ** 2


def calculateCapRegen(maxCapAmount, capRegenTime, currentCapAmount):
    # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
    return 10 * maxCapAmount / capRegenTime * (math.sqrt(currentCapAmount / maxCapAmount) - currentCapAmount / maxCapAmount)
