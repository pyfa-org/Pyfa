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


from abc import ABCMeta, abstractmethod
from collections import OrderedDict, namedtuple


class Graph(metaclass=ABCMeta):

    views = []
    yTypes = None

    @classmethod
    def register(cls):
        Graph.views.append(cls)

    def __init__(self, eosGraph):
        self._eosGraph = eosGraph
        self._cache = {}

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def yDefs(self):
        raise NotImplementedError

    @property
    def yDefMap(self):
        return OrderedDict(((y.handle, y.unit), y) for y in self.yDefs)

    @property
    @abstractmethod
    def xDefs(self):
        raise NotImplementedError

    @property
    def xDefMap(self):
        return OrderedDict(((x.handle, x.unit), x) for x in self.xDefs)

    @property
    def inputs(self):
        raise NotImplementedError

    @property
    def inputMap(self):
        return OrderedDict(((i.handle, i.unit), i) for i in self.inputs)

    @property
    def srcVectorDef(self):
        return None

    @property
    def tgtVectorDef(self):
        return None

    @property
    def hasTargets(self):
        return False

    @property
    def redrawOnEffectiveChange(self):
        return False

    def getPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt=None):
        try:
            plotData = self._cache[fit.ID][(ySpec, xSpec)]
        except KeyError:
            plotData = self._eosGraph.getPlotPoints(mainInput, miscInputs, xSpec, ySpec, fit, tgt)
            fitCache = self._cache.setdefault(fit.ID, {})
            fitCache[(ySpec, xSpec)] = plotData
        return plotData

    def clearCache(self, key=None):
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]
        self._eosGraph.clearCache(key=key)


YDef = namedtuple('YDef', ('handle', 'unit', 'label'))
XDef = namedtuple('XDef', ('handle', 'unit', 'label', 'mainInput'))
Input = namedtuple('Input', ('handle', 'unit', 'label', 'iconID', 'defaultValue', 'defaultRange', 'mainOnly'))
VectorDef = namedtuple('VectorDef', ('lengthHandle', 'lengthUnit', 'angleHandle', 'angleUnit', 'label'))


# noinspection PyUnresolvedReferences
from gui.builtinGraphs import *
