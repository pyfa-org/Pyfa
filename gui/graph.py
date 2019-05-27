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


import re
from abc import ABCMeta, abstractmethod
from collections import namedtuple


class Graph(metaclass=ABCMeta):

    views = []
    yTypes = None

    @classmethod
    def register(cls):
        Graph.views.append(cls)

    def __init__(self):
        self._cache = {}

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def xDef(self):
        raise NotImplementedError

    @property
    def extraInputs(self):
        return {}

    @property
    @abstractmethod
    def yDefs(self):
        raise NotImplementedError

    @property
    def hasTargets(self):
        return False

    @property
    def hasVectors(self):
        return False

    @property
    def redrawOnEffectiveChange(self):
        return False

    def getPlotPoints(self, fit, extraData, xRange, xAmount, yType):
        try:
            plotData = self._cache[fit.ID][yType]
        except KeyError:
            xRange = self.parseRange(xRange)
            extraData = {k: float(v) if v else None for k, v in extraData.items()}
            graph = getattr(self, self.yDefs[yType].eosGraph, None)
            plotData = graph.getPlotPoints(fit, extraData, xRange, xAmount)
            fitCache = self._cache.setdefault(fit.ID, {})
            fitCache[yType] = plotData
        return plotData

    def parseRange(self, string):
        m = re.match('\s*(?P<first>\d+(\.\d+)?)\s*(-\s*(?P<second>\d+(\.\d+)?))?', string)
        if m is None:
            return (0, 0)
        first = float(m.group('first'))
        second = m.group('second')
        second = float(second) if second is not None else 0
        low = min(first, second)
        high = max(first, second)
        return (low, high)

    def clearCache(self, key=None):
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]
        for yDef in self.yDefs.values():
            getattr(self, yDef.eosGraph).clearCache(key=key)


XDef = namedtuple('XDef', ('inputDefault', 'inputLabel', 'inputIconID', 'axisLabel'))
YDef = namedtuple('YDef', ('switchLabel', 'axisLabel', 'eosGraph'))
ExtraInput = namedtuple('ExtraInput', ('inputDefault', 'inputLabel', 'inputIconID'))


# noinspection PyUnresolvedReferences
from gui.builtinGraphs import *
