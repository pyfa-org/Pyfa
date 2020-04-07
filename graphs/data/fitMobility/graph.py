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


from graphs.data.base import FitGraph, XDef, YDef, Input
from .getter import Time2SpeedGetter, Time2DistanceGetter, Time2MomentumGetter, Time2BumpSpeedGetter, Time2BumpDistanceGetter


class FitMobilityGraph(FitGraph):

    # UI stuff
    internalName = 'mobilityGraph'
    name = 'Mobility'
    xDefs = [XDef(handle='time', unit='s', label='Time', mainInput=('time', 's'))]
    yDefs = [
        YDef(handle='speed', unit='m/s', label='Speed'),
        YDef(handle='distance', unit='km', label='Distance'),
        YDef(handle='momentum', unit='Gkg⋅m/s', label='Momentum'),
        YDef(handle='bumpSpeed', unit='m/s', label='Target speed', selectorLabel='Bump speed'),
        YDef(handle='bumpDistance', unit='km', label='Target distance traveled', selectorLabel='Bump distance')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=10, defaultRange=(0, 30)),
        # Default values in target fields correspond to a random carrier/fax
        Input(handle='tgtMass', unit='Mkg', label='Target mass', iconID=76, defaultValue=1300, defaultRange=(100, 2500), conditions=[(None, ('bumpSpeed', 'm/s')), (None, ('bumpDistance', 'km'))], secondaryTooltip='Defined in millions of kilograms'),
        Input(handle='tgtInertia', unit=None, label='Target inertia factor', iconID=1401, defaultValue=0.015, defaultRange=(0.03, 0.1), conditions=[(None, ('bumpDistance', 'km'))], secondaryTooltip='Inertia Modifier attribute value of the target ship')]
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
