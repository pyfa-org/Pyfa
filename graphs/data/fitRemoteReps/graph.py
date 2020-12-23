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

from graphs.data.base import FitGraph, Input, InputCheckbox, XDef, YDef
from service.const import GraphCacheCleanupReason
from .cache import TimeCache
from .getter import Distance2RepAmountGetter, Distance2RpsGetter, Time2RepAmountGetter, Time2RpsGetter

_t = wx.GetTranslation


class FitRemoteRepsGraph(FitGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timeCache = TimeCache()

    def _clearInternalCache(self, reason, extraData):
        # Here, we care only about fit changes, graph changes and option switches
        # - Input changes are irrelevant as time cache cares only about
        # time input, and it regenerates once time goes beyond cached value
        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            self._timeCache.clearForFit(extraData)
        elif reason == GraphCacheCleanupReason.graphSwitched:
            self._timeCache.clearAll()

    # UI stuff
    internalName = 'remoteRepsGraph'
    name = _t('Remote Repairs')
    xDefs = [
        XDef(handle='distance', unit='km', label=_t('Distance'), mainInput=('distance', 'km')),
        XDef(handle='time', unit='s', label=_t('Time'), mainInput=('time', 's'))]
    yDefs = [
        YDef(handle='rps', unit='HP/s', label=_t('Repair speed')),
        YDef(handle='total', unit='HP', label=_t('Total repaired'))]
    inputs = [
        Input(handle='time', unit='s', label=_t('Time'), iconID=1392, defaultValue=None, defaultRange=(0, 80),
              secondaryTooltip=_t('When set, uses repairing ship\'s exact RR stats at a given time\nWhen not set, uses repairing ship\'s RR stats as shown in stats panel of main window')),
        Input(handle='distance', unit='km', label=_t('Distance'), iconID=1391, defaultValue=None, defaultRange=(0, 100),
              mainTooltip=_t('Distance between the repairing ship and the target, as seen in overview (surface-to-surface)'),
              secondaryTooltip=_t('Distance between the repairing ship and the target, as seen in overview (surface-to-surface)'))]
    srcExtraCols = ('ShieldRR', 'ArmorRR', 'HullRR')
    checkboxes = [InputCheckbox(handle='ancReload', label=_t('Reload ancillary RRs'), defaultValue=True)]

    # Calculation stuff
    _normalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v * 1000}
    _limiters = {'time': lambda src, tgt: (0, 2500)}
    _getters = {
        ('distance', 'rps'): Distance2RpsGetter,
        ('distance', 'total'): Distance2RepAmountGetter,
        ('time', 'rps'): Time2RpsGetter,
        ('time', 'total'): Time2RepAmountGetter}
    _denormalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v / 1000}
