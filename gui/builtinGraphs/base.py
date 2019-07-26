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
from collections import OrderedDict, namedtuple

from eos.saveddata.fit import Fit
from eos.saveddata.targetProfile import TargetProfile
from eos.utils.float import floatUnerr
from service.const import GraphCacheCleanupReason


YDef = namedtuple('YDef', ('handle', 'unit', 'label'))
XDef = namedtuple('XDef', ('handle', 'unit', 'label', 'mainInput'))
Input = namedtuple('Input', ('handle', 'unit', 'label', 'iconID', 'defaultValue', 'defaultRange', 'mainOnly'))
VectorDef = namedtuple('VectorDef', ('lengthHandle', 'lengthUnit', 'angleHandle', 'angleUnit', 'label'))


class FitGraph(metaclass=ABCMeta):

    # UI stuff
    views = []
    viewMap = {}

    @classmethod
    def register(cls):
        FitGraph.views.append(cls)
        FitGraph.viewMap[cls.internalName] = cls

    def __init__(self):
        # Format: {(fit ID, target type, target ID): data}
        self._plotCache = {}

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def internalName(self):
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
    def srcExtraCols(self):
        return ()

    @property
    def tgtExtraCols(self):
        return ()

    srcVectorDef = None
    tgtVectorDef = None
    hasTargets = False

    def getPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt=None):
        if isinstance(tgt, Fit):
            tgtType = 'fit'
        elif isinstance(tgt, TargetProfile):
            tgtType = 'profile'
        else:
            tgtType = None
        cacheKey = (fit.ID, tgtType, getattr(tgt, 'ID', None))
        try:
            plotData = self._plotCache[cacheKey][(ySpec, xSpec)]
        except KeyError:
            plotData = self._calcPlotPoints(mainInput, miscInputs, xSpec, ySpec, fit, tgt)
            self._plotCache.setdefault(cacheKey, {})[(ySpec, xSpec)] = plotData
        return plotData

    def clearCache(self, reason, extraData=None):
        # If only one fit changed - clear plots which concern this fit
        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            # Clear plot cache
            plotKeysToClear = set()
            for cacheKey in self._plotCache:
                cacheFitID, cacheTgtType, cacheTgtID = cacheKey
                if extraData == cacheFitID:
                    plotKeysToClear.add(cacheKey)
                elif cacheTgtType == 'fit' and extraData == cacheTgtID:
                    plotKeysToClear.add(cacheKey)
            for cacheKey in plotKeysToClear:
                del self._plotCache[cacheKey]
        # Wipe out whole plot cache otherwise
        else:
            self._plotCache.clear()
        # And process any internal caches graphs might have
        self._clearInternalCache(reason, extraData)

    def _clearInternalCache(self, reason, extraData):
        return

    # Calculation stuff
    def _calcPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt):
        mainParam, miscParams = self._normalizeParams(mainInput, miscInputs, fit, tgt)
        mainParam, miscParams = self._limitParams(mainParam, miscParams, fit, tgt)
        xs, ys = self._getPoints(mainParam, miscParams, xSpec, ySpec, fit, tgt)
        ys = self._denormalizeValues(ys, ySpec, fit, tgt)
        # Sometimes x denormalizer may fail (e.g. during conversion of 0 ship speed to %).
        # If both inputs and outputs are in %, do some extra processing to at least have
        # proper graph which shows that fit has the same value over whole specified
        # relative parameter range
        try:
            xs = self._denormalizeValues(xs, xSpec, fit, tgt)
        except ZeroDivisionError:
            if mainInput.unit == xSpec.unit == '%' and len(set(floatUnerr(y) for y in ys)) == 1:
                xs = [min(mainInput.value), max(mainInput.value)]
                ys = [ys[0], ys[0]]
            else:
                raise
        # Same for NaN which means we tried to denormalize infinity values, which might be the
        # case for the ideal target profile with infinite signature radius
        if mainInput.unit == xSpec.unit == '%' and all(math.isnan(x) for x in xs):
            xs = [min(mainInput.value), max(mainInput.value)]
            ys = [ys[0], ys[0]]
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
                newMiscInput = (miscInput.handle, normalizer(miscInput.value, fit, tgt))
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

    def _iterLinear(self, valRange, segments=200):
        rangeLow = min(valRange)
        rangeHigh = max(valRange)
        # Amount is amount of ranges between points here, not amount of points
        step = (rangeHigh - rangeLow) / segments
        if step == 0 or math.isnan(step):
            yield rangeLow
        else:
            current = rangeLow
            # Take extra half step to make sure end of range is always included
            # despite any possible float errors
            while current <= (rangeHigh + step / 2):
                yield current
                current += step


class FitDataCache:

    def __init__(self):
        self._data = {}

    def clearForFit(self, fitID):
        if fitID in self._data:
            del self._data[fitID]

    def clearAll(self):
        self._data.clear()


# noinspection PyUnresolvedReferences
from gui.builtinGraphs import *
