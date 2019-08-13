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


from graphs.data.base import FitGraph, Input, XDef, YDef
from .getter import Distance2WebbingStrengthGetter


class FitEwarStatsGraph(FitGraph):

    # UI stuff
    internalName = 'ewarStatsGraph'
    name = 'Electronic Warfare Stats'
    xDefs = [XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km'))]
    yDefs = [YDef(handle='webStr', unit='%', label='Webbing strength')]
    inputs = [
        Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=None, defaultRange=(0, 100)),
        Input(handle='resist', unit='%', label='Target resistance', iconID=1393, defaultValue=0, defaultRange=(0, 100))]

    # Calculation stuff
    _normalizers = {
        ('distance', 'km'): lambda v, src, tgt: None if v is None else v * 1000,
        ('resist', '%'): lambda v, src, tgt: None if v is None else v / 100}
    _limiters = {'resist': lambda src, tgt: (0, 1)}
    _getters = {('distance', 'webStr'): Distance2WebbingStrengthGetter}
    _denormalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v / 1000}
