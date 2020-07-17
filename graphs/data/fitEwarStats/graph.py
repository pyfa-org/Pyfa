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
from .getter import (Distance2DampStrLockRangeGetter, Distance2EcmStrMaxGetter, Distance2GdStrRangeGetter, Distance2NeutingStrGetter, Distance2TdStrOptimalGetter,
                     Distance2TpStrGetter, Distance2WebbingStrGetter)

_t = wx.GetTranslation


class FitEwarStatsGraph(FitGraph):
    # UI stuff
    internalName = 'ewarStatsGraph'
    name = _t('Electronic Warfare Stats')
    xDefs = [XDef(handle='distance', unit='km', label=_t('Distance'), mainInput=('distance', 'km'))]
    yDefs = [
        YDef(handle='neutStr', unit=None, label=_t('Cap neutralized per second'), selectorLabel=_t('Neuts: cap per second')),
        YDef(handle='webStr', unit='%', label=_t('Speed reduction'), selectorLabel=_t('Webs: speed reduction')),
        YDef(handle='ecmStrMax', unit=None, label=_t('Combined ECM strength'), selectorLabel=_t('ECM: combined strength')),
        YDef(handle='dampStrLockRange', unit='%', label=_t('Lock range reduction'), selectorLabel=_t('Damps: lock range reduction')),
        YDef(handle='tdStrOptimal', unit='%', label=_t('Turret optimal range reduction'), selectorLabel=_t('TDs: turret optimal range reduction')),
        YDef(handle='gdStrRange', unit='%', label=_t('Missile flight range reduction'), selectorLabel=_t('GDs: missile flight range reduction')),
        YDef(handle='tpStr', unit='%', label=_t('Signature radius increase'), selectorLabel=_t('TPs: signature radius increase'))]
    inputs = [
        Input(handle='distance', unit='km', label=_t('Distance'), iconID=1391, defaultValue=None, defaultRange=(0, 100)),
        Input(handle='resist', unit='%', label=_t('Target resistance'), iconID=1393, defaultValue=0, defaultRange=(0, 100))]

    # Calculation stuff
    _normalizers = {
        ('distance', 'km'): lambda v, src, tgt: None if v is None else v * 1000,
        ('resist', '%'): lambda v, src, tgt: None if v is None else v / 100}
    _limiters = {'resist': lambda src, tgt: (0, 1)}
    _getters = {
        ('distance', 'neutStr'): Distance2NeutingStrGetter,
        ('distance', 'webStr'): Distance2WebbingStrGetter,
        ('distance', 'ecmStrMax'): Distance2EcmStrMaxGetter,
        ('distance', 'dampStrLockRange'): Distance2DampStrLockRangeGetter,
        ('distance', 'tdStrOptimal'): Distance2TdStrOptimalGetter,
        ('distance', 'gdStrRange'): Distance2GdStrRangeGetter,
        ('distance', 'tpStr'): Distance2TpStrGetter}
    _denormalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v / 1000}
