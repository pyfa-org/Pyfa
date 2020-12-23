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
from .getter import Time2BumpDistanceGetter, Time2BumpSpeedGetter, Time2DistanceGetter, Time2MomentumGetter, Time2SpeedGetter

_t = wx.GetTranslation


class FitMobilityGraph(FitGraph):
    # UI stuff
    internalName = 'mobilityGraph'
    name = _t('Mobility')
    xDefs = [XDef(handle='time', unit='s', label=_t('Time'), mainInput=('time', 's'))]
    yDefs = [
        YDef(handle='speed', unit='m/s', label=_t('Speed')),
        YDef(handle='distance', unit='km', label=_t('Distance')),
        YDef(handle='momentum', unit='Gkg⋅m/s', label=_t('Momentum')),
        YDef(handle='bumpSpeed', unit='m/s', label=_t('Target speed'), selectorLabel=_t('Bump speed')),
        YDef(handle='bumpDistance', unit='km', label=_t('Target distance traveled'), selectorLabel=_t('Bump distance'))]
    inputs = [
        Input(handle='time', unit='s', label=_t('Time'), iconID=1392, defaultValue=10, defaultRange=(0, 30)),
        # Default values in target fields correspond to a random carrier/fax
        Input(handle='tgtMass', unit='Mkg', label=_t('Target mass'), iconID=76, defaultValue=1300, defaultRange=(100, 2500),
              conditions=[(None, ('bumpSpeed', 'm/s')), (None, ('bumpDistance', 'km'))], secondaryTooltip=_t('Defined in millions of kilograms')),
        Input(handle='tgtInertia', unit=None, label=_t('Target inertia factor'), iconID=1401, defaultValue=0.015, defaultRange=(0.03, 0.1),
              conditions=[(None, ('bumpDistance', 'km'))], secondaryTooltip=_t('Inertia Modifier attribute value of the target ship'))]
    srcExtraCols = ('Speed', 'Agility')

    # Calculation stuff
    _normalizers = {('tgtMass', 'Mkg'): lambda v, src, tgt: None if v is None else v * 10 ** 6}
    _getters = {
        ('time', 'speed'): Time2SpeedGetter,
        ('time', 'distance'): Time2DistanceGetter,
        ('time', 'momentum'): Time2MomentumGetter,
        ('time', 'bumpSpeed'): Time2BumpSpeedGetter,
        ('time', 'bumpDistance'): Time2BumpDistanceGetter}
    _denormalizers = {
        ('distance', 'km'): lambda v, src, tgt: v / 1000,
        ('momentum', 'Gkg⋅m/s'): lambda v, src, tgt: v / 10 ** 9,
        ('bumpDistance', 'km'): lambda v, src, tgt: v / 1000}
