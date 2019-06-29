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


YDef = namedtuple('YDef', ('handle', 'unit', 'label'))
XDef = namedtuple('XDef', ('handle', 'unit', 'label', 'mainInput'))
Input = namedtuple('Input', ('handle', 'unit', 'label', 'iconID', 'defaultValue', 'defaultRange', 'mainOnly'))
VectorDef = namedtuple('VectorDef', ('lengthHandle', 'lengthUnit', 'angleHandle', 'angleUnit', 'label'))


class FitGraph(metaclass=ABCMeta):

    # UI stuff
    views = []

    @classmethod
    def register(cls):
        FitGraph.views.append(cls)

    def __init__(self):
        self._plotCache = {}
        self._calcCache = {}

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

    srcVectorDef = None
    tgtVectorDef = None
    hasTargets = False

    def getPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt=None):
        try:
            plotData = self._plotCache[fit.ID][(ySpec, xSpec)]
        except KeyError:
            plotData = self._calcPlotPoints(mainInput, miscInputs, xSpec, ySpec, fit, tgt)
            fitCache = self._plotCache.setdefault(fit.ID, {})
            fitCache[(ySpec, xSpec)] = plotData
        return plotData

    def clearCache(self, key=None):
        if key is None:
            self._plotCache.clear()
            self._calcCache.clear()
        if key in self._plotCache:
            del self._plotCache[key]
        if key in self._calcCache:
            del self._calcCache[key]

    # Calculation stuff
    def _calcPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt):
        mainInput, miscInputs = self._normalizeParams(mainInput, miscInputs, fit, tgt)
        mainInput, miscInputs = self._limitParams(mainInput, miscInputs, fit, tgt)
        xs, ys = self._getPoints(mainInput, miscInputs, xSpec, ySpec, fit, tgt)
        xs = self._denormalizeValues(xs, xSpec, fit, tgt)
        ys = self._denormalizeValues(ys, ySpec, fit, tgt)
        return xs, ys

    _normalizers = {}

    def _normalizeParams(self, mainInput, miscInputs, fit, tgt):
        key = (mainInput.handle, mainInput.unit)
        if key in self._normalizers:
            normalizer = self._normalizers[key]
            newMainInput = (mainInput.handle, tuple(normalizer(v, fit, tgt) for v in mainInput.value))
        else:
            newMainInput = (mainInput.handle, mainInput.value)
        newMiscInputs = []
        for miscInput in miscInputs:
            key = (miscInput.handle, miscInput.unit)
            if key in self._normalizers:
                normalizer = self._normalizers[key]
                newMiscInput = (miscInput.handle, normalizer(miscInput.value))
            else:
                newMiscInput = (miscInput.handle, miscInput.value)
            newMiscInputs.append(newMiscInput)
        return newMainInput, newMiscInputs

    _limiters = {}

    def _limitParams(self, mainInput, miscInputs, fit, tgt):

        def limitToRange(val, limitRange):
            if val is None:
                return None
            val = max(val, min(limitRange))
            val = min(val, max(limitRange))
            return val

        mainHandle, mainValue = mainInput
        if mainHandle in self._limiters:
            limiter = self._limiters[mainHandle]
            newMainInput = (mainHandle, tuple(limitToRange(v, limiter(fit, tgt)) for v in mainValue))
        else:
            newMainInput = mainInput
        newMiscInputs = []
        for miscInput in miscInputs:
            miscHandle, miscValue = miscInput
            if miscHandle in self._limiters:
                limiter = self._limiters[miscHandle]
                newMiscInput = (miscHandle, limitToRange(miscValue, limiter(fit, tgt)))
                newMiscInputs.append(newMiscInput)
            else:
                newMiscInputs.append(miscInput)
        return newMainInput, newMiscInputs

    _getters = {}

    def _getPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt):
        try:
            getter = self._getters[(xSpec.handle, ySpec.handle)]
        except KeyError:
            return [], []
        else:
            return getter(self, mainInput, miscInputs, fit, tgt)

    _denormalizers = {}

    def _denormalizeValues(self, values, axisSpec, fit, tgt):
        key = (axisSpec.handle, axisSpec.unit)
        if key in self._denormalizers:
            denormalizer = self._denormalizers[key]
            values = [denormalizer(v, fit, tgt) for v in values]
        return values

    def _iterLinear(self, valRange, resolution=200):
        rangeLow = min(valRange)
        rangeHigh = max(valRange)
        # Amount is amount of ranges between points here, not amount of points
        step = (rangeHigh - rangeLow) / resolution
        if step == 0:
            yield rangeLow
        else:
            current = rangeLow
            # Take extra half step to make sure end of range is always included
            # despite any possible float errors
            while current <= (rangeHigh + step / 2):
                yield current
                current += step


# noinspection PyUnresolvedReferences
from gui.builtinGraphs import *
