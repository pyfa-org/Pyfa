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


from collections import OrderedDict

from eos.graph.fitWarpTimeVsDistance import FitWarpTimeVsDistanceGraph as EosGraph
from gui.graph import Graph, XDef, YDef


class FitWarpTimeVsDistanceGraph(Graph):

    name = 'Warp Time vs Distance'

    def __init__(self):
        self.eosGraph = EosGraph()

    @property
    def xDef(self):
        return XDef(inputDefault='0-50', inputLabel='Distance (AU)', inputIconID=1391, axisLabel='Warp distance, AU')

    @property
    def yDefs(self):
        return OrderedDict([('time', YDef(switchLabel='Warp time', axisLabel='Warp time, s', eosGraph='eosGraph'))])


FitWarpTimeVsDistanceGraph.register()
