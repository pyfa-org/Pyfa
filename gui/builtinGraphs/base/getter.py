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
from abc import ABCMeta, abstractmethod


class PointGetter(metaclass=ABCMeta):

    def __init__(self, graph):
        self.graph = graph

    @abstractmethod
    def getRange(self, mainParamRange, miscParams, fit, tgt):
        raise NotImplementedError

    @abstractmethod
    def getPoint(self, mainParam, miscParams, fit, tgt):
        raise NotImplementedError


class SmoothPointGetter(PointGetter, metaclass=ABCMeta):

    def __init__(self, graph, baseResolution=50, extraDepth=2):
        super().__init__(graph)
        self._baseResolution = baseResolution
        self._extraDepth = extraDepth

    def getRange(self, mainParamRange, miscParams, fit, tgt):
        xs = []
        ys = []
        commonData = self._getCommonData(miscParams=miscParams, fit=fit, tgt=tgt)

        def addExtraPoints(leftX, leftY, rightX, rightY, depth):
            if depth > 0 and leftY != rightY:
                newX = (leftX + rightX) / 2
                newY = self._calculatePoint(x=newX, miscParams=miscParams, fit=fit, tgt=tgt, commonData=commonData)
                addExtraPoints(leftX=prevX, leftY=prevY, rightX=newX, rightY=newY, depth=depth - 1)
                xs.append(newX)
                ys.append(newY)
                addExtraPoints(leftX=newX, leftY=newY, rightX=rightX, rightY=rightY, depth=depth - 1)

        # Format: {depth level: last value on that level}
        prevX = None
        prevY = None
        # Go through X points defined by our resolution setting
        for x in self._iterLinear(mainParamRange[1]):
            y = self._calculatePoint(x=x, miscParams=miscParams, fit=fit, tgt=tgt, commonData=commonData)
            if prevX is not None and prevY is not None:
                # And if Y values of adjacent data points are not equal, add extra points
                # depending on extra depth setting
                addExtraPoints(leftX=prevX, leftY=prevY, rightX=x, rightY=y, depth=self._extraDepth)
            prevX = x
            prevY = y
            xs.append(x)
            ys.append(y)
        return xs, ys

    def getPoint(self, mainParam, miscParams, fit, tgt):
        commonData = self._getCommonData(miscParams=miscParams, fit=fit, tgt=tgt)
        x = mainParam[1]
        y = self._calculatePoint(x=x, miscParams=miscParams, fit=fit, tgt=tgt, commonData=commonData)
        return x, y

    def _iterLinear(self, valRange):
        rangeLow = min(valRange)
        rangeHigh = max(valRange)
        # Resolution defines amount of ranges between points here,
        # not amount of points
        step = (rangeHigh - rangeLow) / self._baseResolution
        if step == 0 or math.isnan(step):
            yield rangeLow
        else:
            current = rangeLow
            # Take extra half step to make sure end of range is always included
            # despite any possible float errors
            while current <= (rangeHigh + step / 2):
                yield current
                current += step

    def _getCommonData(self, miscParams, fit, tgt):
        return {}

    @abstractmethod
    def _calculatePoint(self, x, miscParams, fit, tgt, commonData):
        raise NotImplementedError
