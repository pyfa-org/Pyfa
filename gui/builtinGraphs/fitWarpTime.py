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


from eos.graph.fitWarpTime import FitWarpTimeGraph as EosGraph
from .base import Graph, XDef, YDef, Input


class FitWarpTimeGraph(Graph):

    name = 'Warp Time'

    def __init__(self):
        super().__init__(EosGraph())

    @property
    def xDefs(self):
        return [
            XDef(handle='distance', unit='AU', label='Distance', mainInput=('distance', 'AU')),
            XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km'))]

    @property
    def yDefs(self):
        return [YDef(handle='time', unit='s', label='Warp time')]

    @property
    def inputs(self):
        return [
            Input(handle='distance', unit='AU', label='Distance', iconID=1391, defaultValue=50, defaultRange=(0, 50), mainOnly=False),
            Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=10000, defaultRange=(150, 5000), mainOnly=False)]


FitWarpTimeGraph.register()
