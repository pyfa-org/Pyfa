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


import wx

from graphs.data.base import FitGraph, Input, XDef, YDef
from service.const import GraphCacheCleanupReason
from .cache import SubwarpSpeedCache
from .getter import AU_METERS, Distance2TimeGetter

_t = wx.GetTranslation


class FitWarpTimeGraph(FitGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subspeedCache = SubwarpSpeedCache()

    def _clearInternalCache(self, reason, extraData):
        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            self._subspeedCache.clearForFit(extraData)
        elif reason == GraphCacheCleanupReason.graphSwitched:
            self._subspeedCache.clearAll()

    # UI stuff
    internalName = 'warpTimeGraph'
    name = _t('Warp Time')
    xDefs = [
        XDef(handle='distance', unit='AU', label=_t('Distance'), mainInput=('distance', 'AU')),
        XDef(handle='distance', unit='km', label=_t('Distance'), mainInput=('distance', 'km'))]
    yDefs = [YDef(handle='time', unit='s', label=_t('Warp time'))]
    inputs = [
        Input(handle='distance', unit='AU', label=_t('Distance'), iconID=1391, defaultValue=20, defaultRange=(0, 50)),
        Input(handle='distance', unit='km', label=_t('Distance'), iconID=1391, defaultValue=1000, defaultRange=(150, 5000))]
    srcExtraCols = ('WarpSpeed', 'WarpDistance')

    # Calculation stuff
    _normalizers = {
        ('distance', 'AU'): lambda v, src, tgt: v * AU_METERS,
        ('distance', 'km'): lambda v, src, tgt: v * 1000
    }
    _limiters = {'distance': lambda src, tgt: (0, src.item.maxWarpDistance * AU_METERS)}
    _getters = {('distance', 'time'): Distance2TimeGetter}
    _denormalizers = {
        ('distance', 'AU'): lambda v, src, tgt: v / AU_METERS,
        ('distance', 'km'): lambda v, src, tgt: v / 1000}
