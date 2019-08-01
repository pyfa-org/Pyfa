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
VectorDef = namedtuple('VectorDef', ('lengthHandle', 'lengthUnit', 'angleHandle', 'angleUnit', 'label'))


class Input:

    def __init__(self, handle, unit, label, iconID, defaultValue, defaultRange, mainOnly=False, mainTooltip=None, secondaryTooltip=None):
        self.handle = handle
        self.unit = unit
        self.label = label
        self.iconID = iconID
        self.defaultValue = defaultValue
        self.defaultRange = defaultRange
        self.mainOnly = mainOnly
        self.mainTooltip = mainTooltip
        self.secondaryTooltip = secondaryTooltip


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
        plotKeysToClear = set()
        # If fit changed - clear plots which concern this fit
        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            for cacheKey in self._plotCache:
                cacheFitID, cacheTgtType, cacheTgtID = cacheKey
                if extraData == cacheFitID:
                    plotKeysToClear.add(cacheKey)
                elif cacheTgtType == 'fit' and extraData == cacheTgtID:
                    plotKeysToClear.add(cacheKey)
        # Same for profile
        elif reason in (GraphCacheCleanupReason.profileChanged, GraphCacheCleanupReason.profileRemoved):
            for cacheKey in self._plotCache:
                cacheFitID, cacheTgtType, cacheTgtID = cacheKey
                if cacheTgtType == 'profile' and extraData == cacheTgtID:
                    plotKeysToClear.add(cacheKey)
        # Wipe out whole plot cache otherwise
        else:
            for cacheKey in self._plotCache:
                plotKeysToClear.add(cacheKey)
        # Do actual cleanup
        for cacheKey in plotKeysToClear:
            del self._plotCache[cacheKey]
        # Process any internal caches graphs might have
        self._clearInternalCache(reason, extraData)

    def _clearInternalCache(self, reason, extraData):
        return

    # Calculation stuff
    def _calcPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, fit, tgt):
        mainParam, miscParams = self._normalizeInputs(mainInput=mainInput, miscInputs=miscInputs, fit=fit, tgt=tgt)
        mainParam, miscParams = self._limitParams(mainParam=mainParam, miscParams=miscParams, fit=fit, tgt=tgt)
        xs, ys = self._getPoints(mainParam=mainParam, miscParams=miscParams, xSpec=xSpec, ySpec=ySpec, fit=fit, tgt=tgt)
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
        else:
            # Same for NaN which means we tried to denormalize infinity values, which might be the
            # case for the ideal target profile with infinite signature radius
            if mainInput.unit == xSpec.unit == '%' and all(math.isnan(x) for x in xs):
                xs = [min(mainInput.value), max(mainInput.value)]
                ys = [ys[0], ys[0]]
        return xs, ys

    _normalizers = {}

    def _normalizeInputs(self, mainInput, miscInputs, fit, tgt):
        key = (mainInput.handle, mainInput.unit)
        if key in self._normalizers:
            normalizer = self._normalizers[key]
            mainParam = (mainInput.handle, tuple(normalizer(v, fit, tgt) for v in mainInput.value))
        else:
            mainParam = (mainInput.handle, mainInput.value)
        miscParams = []
        for miscInput in miscInputs:
            key = (miscInput.handle, miscInput.unit)
            if key in self._normalizers:
                normalizer = self._normalizers[key]
                miscParam = (miscInput.handle, normalizer(miscInput.value, fit, tgt))
            else:
                miscParam = (miscInput.handle, miscInput.value)
            miscParams.append(miscParam)
        return mainParam, miscParams

    _limiters = {}

    def _limitParams(self, mainParam, miscParams, fit, tgt):

        def limitToRange(val, limitRange):
            if val is None:
                return None
            val = max(val, min(limitRange))
            val = min(val, max(limitRange))
            return val

        mainHandle, mainValue = mainParam
        if mainHandle in self._limiters:
            limiter = self._limiters[mainHandle]
            newMainParam = (mainHandle, tuple(limitToRange(v, limiter(fit, tgt)) for v in mainValue))
        else:
            newMainParam = mainParam
        newMiscParams = []
        for miscParam in miscParams:
            miscHandle, miscValue = miscParam
            if miscHandle in self._limiters:
                limiter = self._limiters[miscHandle]
                newMiscParam = (miscHandle, limitToRange(miscValue, limiter(fit, tgt)))
                newMiscParams.append(newMiscParam)
            else:
                newMiscParams.append(miscParam)
        return newMainParam, newMiscParams

    _getters = {}

    def _getPoints(self, mainParam, miscParams, xSpec, ySpec, fit, tgt):
        try:
            fullGetter, singleGetter, cacheGetter = self._getters[(xSpec.handle, ySpec.handle)]
        except KeyError:
            return [], []
        else:
            return fullGetter(
                self, cacheGetter=cacheGetter, singleGetter=singleGetter,
                mainParam=mainParam, miscParams=miscParams, fit=fit, tgt=tgt)

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
