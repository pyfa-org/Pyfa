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

    def __init__(self, graph, baseResolution=200):
        super().__init__(graph)
        self._baseResolution = baseResolution

    def getRange(self, mainParamRange, miscParams, fit, tgt):
        xs = []
        ys = []
        commonData = self._getCommonData(miscParams=miscParams, fit=fit, tgt=tgt)
        for x in self._iterLinear(mainParamRange[1]):
            y = self._calculatePoint(x=x, miscParams=miscParams, fit=fit, tgt=tgt, commonData=commonData)
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
