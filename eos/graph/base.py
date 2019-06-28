# ===============================================================================
# Copyright (C) 2010 Diego Duclos
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


import math
from abc import ABCMeta, abstractmethod


class Graph(metaclass=ABCMeta):

    def __init__(self):
        self._cache = {}



    ### Old stuff

    def getYForX(self, x, miscInputs, xSpec, ySpec, fit, tgt):
        raise NotImplementedError

    def _xIter(self, fit, extraData, xRange, xAmount):
        rangeLow, rangeHigh = self._limitXRange(xRange, fit, extraData)
        # Amount is amount of ranges between points here, not amount of points
        step = (rangeHigh - rangeLow) / xAmount
        if step == 0:
            yield xRange[0]
        else:
            current = rangeLow
            # Take extra half step to make sure end of range is always included
            # despite any possible float errors
            while current <= (rangeHigh + step / 2):
                yield current
                current += step

    def _limitXRange(self, xRange, fit, extraData):
        rangeLow, rangeHigh = sorted(xRange)
        limitLow, limitHigh = self._getXLimits(fit, extraData)
        rangeLow = max(limitLow, rangeLow)
        rangeHigh = min(limitHigh, rangeHigh)
        return rangeLow, rangeHigh

    def _getInputLimits(self, inputHandle, inputUnit, fit):
        return -math.inf, math.inf

    def clearCache(self, key=None):
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]


class SmoothGraph(Graph, metaclass=ABCMeta):

    def getPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt):
        xs = []
        ys = []
        for x in self._xIter(fit, extraData, xRange, xAmount):
            xs.append(x)
            ys.append(self.getYForX(fit, extraData, x))
        return xs, ys
