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
from .getter import Time2SpeedGetter, Time2DistanceGetter, Time2MomentumGetter


class FitMobilityGraph(FitGraph):

    # UI stuff
    internalName = 'mobilityGraph'
    name = 'Mobility'
    xDefs = [XDef(handle='time', unit='s', label='Time', mainInput=('time', 's'))]
    yDefs = [
        YDef(handle='speed', unit='m/s', label='Speed'),
        YDef(handle='distance', unit='km', label='Distance'),
        YDef(handle='momentum', unit='Mt⋅m/s', label='Momentum')]
    inputs = [Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=10, defaultRange=(0, 30))]
    srcExtraCols = ('Speed', 'Agility')

    # Calculation stuff
    _getters = {
        ('time', 'speed'): Time2SpeedGetter,
        ('time', 'distance'): Time2DistanceGetter,
        ('time', 'momentum'): Time2MomentumGetter}
    _denormalizers = {
        ('distance', 'km'): lambda v, src, tgt: v / 1000,
        ('momentum', 'Mt⋅m/s'): lambda v, src, tgt: v / 10 ** 9}
