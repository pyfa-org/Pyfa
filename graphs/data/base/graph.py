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
from collections import OrderedDict

from eos.utils.float import floatUnerr
from service.const import GraphCacheCleanupReason


class FitGraph(metaclass=ABCMeta):

    # UI stuff
    hidden = False
    views = []
    viewMap = {}

    @classmethod
    def register(cls):
        FitGraph.views.append(cls)
        FitGraph.viewMap[cls.internalName] = cls

    def __init__(self):
        # Format: {(fit ID, target type, target ID): {(xSpec, ySpec): (xs, ys)}}
        self._plotCache = {}
        # Format: {(fit ID, target type, target ID): {(xSpec, ySpec): {x: y}}}
        self._pointCache = {}

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

    checkboxes = ()

    @property
    def checkboxesMap(self):
        return OrderedDict((ec.handle, ec) for ec in self.checkboxes)

    hasTargets = False
    srcVectorDef = None
    tgtVectorDef = None
    srcExtraCols = ()
    tgtExtraCols = ()
    usesHpEffectivity = False

    def getPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, src, tgt=None):
        cacheKey = self._makeCacheKey(src=src, tgt=tgt)
        try:
            plotData = self._plotCache[cacheKey][(ySpec, xSpec)]
        except KeyError:
            plotData = self._calcPlotPoints(
                mainInput=mainInput, miscInputs=miscInputs,
                xSpec=xSpec, ySpec=ySpec, src=src, tgt=tgt)
            self._plotCache.setdefault(cacheKey, {})[(ySpec, xSpec)] = plotData
        return plotData

    def getPoint(self, x, miscInputs, xSpec, ySpec, src, tgt=None):
        cacheKey = self._makeCacheKey(src=src, tgt=tgt)
        try:
            y = self._pointCache[cacheKey][(ySpec, xSpec)][x]
        except KeyError:
            y = self._calcPoint(x=x, miscInputs=miscInputs, xSpec=xSpec, ySpec=ySpec, src=src, tgt=tgt)
            self._pointCache.setdefault(cacheKey, {}).setdefault((ySpec, xSpec), {})[x] = y
        return y

    def clearCache(self, reason, extraData=None):
        caches = (self._plotCache, self._pointCache)
        plotKeysToClear = set()
        # If fit changed - clear plots which concern this fit
        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            for cache in caches:
                for cacheKey in cache:
                    cacheFitID, cacheTgtType, cacheTgtID = cacheKey
                    if extraData == cacheFitID:
                        plotKeysToClear.add(cacheKey)
                    elif cacheTgtType == 'fit' and extraData == cacheTgtID:
                        plotKeysToClear.add(cacheKey)
        # Same for profile
        elif reason in (GraphCacheCleanupReason.profileChanged, GraphCacheCleanupReason.profileRemoved):
            for cache in caches:
                for cacheKey in cache:
                    cacheFitID, cacheTgtType, cacheTgtID = cacheKey
                    if cacheTgtType == 'profile' and extraData == cacheTgtID:
                        plotKeysToClear.add(cacheKey)
        # Target fit resist mode changed
        elif reason == GraphCacheCleanupReason.resistModeChanged:
            for cache in caches:
                for cacheKey in cache:
                    cacheFitID, cacheTgtType, cacheTgtID = cacheKey
                    if cacheTgtType == 'fit' and extraData == cacheTgtID:
                        plotKeysToClear.add(cacheKey)
        # Wipe out whole plot cache otherwise
        else:
            for cache in caches:
                for cacheKey in cache:
                    plotKeysToClear.add(cacheKey)
        # Do actual cleanup
        for cache in caches:
            for cacheKey in plotKeysToClear:
                try:
                    del cache[cacheKey]
                except KeyError:
                    pass
        # Process any internal caches graphs might have
        self._clearInternalCache(reason, extraData)

    def _makeCacheKey(self, src, tgt):
        if tgt is not None and tgt.isFit:
            tgtType = 'fit'
            tgtItemID = tgt.item.ID
        elif tgt is not None and tgt.isProfile:
            tgtType = 'profile'
            tgtItemID = tgt.item.ID
        else:
            tgtType = None
            tgtItemID = None
        cacheKey = (src.item.ID, tgtType, tgtItemID)
        return cacheKey

    def _clearInternalCache(self, reason, extraData):
        return

    # Calculation stuff
    def _calcPlotPoints(self, mainInput, miscInputs, xSpec, ySpec, src, tgt):
        mainParamRange = self._normalizeMain(mainInput=mainInput, src=src, tgt=tgt)
        miscParams = self._normalizeMisc(miscInputs=miscInputs, src=src, tgt=tgt)
        mainParamRange = self._limitMain(mainParamRange=mainParamRange, src=src, tgt=tgt)
        miscParams = self._limitMisc(miscParams=miscParams, src=src, tgt=tgt)
        xs, ys = self._getPlotPoints(
            xRange=mainParamRange[1], miscParams=miscParams,
            xSpec=xSpec, ySpec=ySpec, src=src, tgt=tgt)
        ys = self._denormalizeValues(values=ys, axisSpec=ySpec, src=src, tgt=tgt)
        # Sometimes x denormalizer may fail (e.g. during conversion of 0 ship speed to %).
        # If both inputs and outputs are in %, do some extra processing to at least have
        # proper graph which shows the same value over whole specified relative parameter
        # range
        try:
            xs = self._denormalizeValues(values=xs, axisSpec=xSpec, src=src, tgt=tgt)
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

    def _calcPoint(self, x, miscInputs, xSpec, ySpec, src, tgt):
        x = self._normalizeValue(value=x, axisSpec=xSpec, src=src, tgt=tgt)
        miscParams = self._normalizeMisc(miscInputs=miscInputs, src=src, tgt=tgt)
        miscParams = self._limitMisc(miscParams=miscParams, src=src, tgt=tgt)
        y = self._getPoint(x=x, miscParams=miscParams, xSpec=xSpec, ySpec=ySpec, src=src, tgt=tgt)
        y = self._denormalizeValue(value=y, axisSpec=ySpec, src=src, tgt=tgt)
        return y

    _normalizers = {}

    def _normalizeMain(self, mainInput, src, tgt):
        key = (mainInput.handle, mainInput.unit)
        if key in self._normalizers:
            normalizer = self._normalizers[key]
            mainParamRange = (mainInput.handle, tuple(normalizer(v, src, tgt) for v in mainInput.value))
        else:
            mainParamRange = (mainInput.handle, mainInput.value)
        return mainParamRange

    def _normalizeMisc(self, miscInputs, src, tgt):
        miscParams = {}
        for miscInput in miscInputs:
            key = (miscInput.handle, miscInput.unit)
            if key in self._normalizers:
                normalizer = self._normalizers[key]
                miscParams[miscInput.handle] = normalizer(miscInput.value, src, tgt)
            else:
                miscParams[miscInput.handle] = miscInput.value
        return miscParams

    def _normalizeValue(self, value, axisSpec, src, tgt):
        key = (axisSpec.handle, axisSpec.unit)
        if key in self._normalizers:
            normalizer = self._normalizers[key]
            value = normalizer(value, src, tgt)
        return value

    _limiters = {}

    def _limitMain(self, mainParamRange, src, tgt):
        mainHandle, mainValue = mainParamRange
        if mainHandle in self._limiters:
            limiter = self._limiters[mainHandle]
            mainParamRange = (mainHandle, tuple(self.__limitToRange(v, limiter(src, tgt)) for v in mainValue))
        return mainParamRange

    def _limitMisc(self, miscParams, src, tgt):
        for miscHandle in miscParams:
            if miscHandle in self._limiters:
                limiter = self._limiters[miscHandle]
                miscValue = miscParams[miscHandle]
                miscParams[miscHandle] = self.__limitToRange(miscValue, limiter(src, tgt))
        return miscParams

    @staticmethod
    def __limitToRange(val, limitRange):
        if val is None:
            return None
        val = max(val, min(limitRange))
        val = min(val, max(limitRange))
        return val

    _getters = {}

    def _getPlotPoints(self, xRange, miscParams, xSpec, ySpec, src, tgt):
        try:
            getterClass = self._getters[(xSpec.handle, ySpec.handle)]
        except KeyError:
            return [], []
        else:
            getter = getterClass(graph=self)
            return getter.getRange(xRange=xRange, miscParams=miscParams, src=src, tgt=tgt)

    def _getPoint(self, x, miscParams, xSpec, ySpec, src, tgt):
        try:
            getterClass = self._getters[(xSpec.handle, ySpec.handle)]
        except KeyError:
            return [], []
        else:
            getter = getterClass(graph=self)
            return getter.getPoint(x=x, miscParams=miscParams, src=src, tgt=tgt)

    _denormalizers = {}

    def _denormalizeValues(self, values, axisSpec, src, tgt):
        key = (axisSpec.handle, axisSpec.unit)
        if key in self._denormalizers:
            denormalizer = self._denormalizers[key]
            values = [denormalizer(v, src, tgt) for v in values]
        return values

    def _denormalizeValue(self, value, axisSpec, src, tgt):
        key = (axisSpec.handle, axisSpec.unit)
        if key in self._denormalizers:
            denormalizer = self._denormalizers[key]
            value = denormalizer(value, src, tgt)
        return value
