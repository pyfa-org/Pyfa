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

from eos.graph.fitDmgVsTime import FitDmgVsTimeGraph as EosGraphDmg
from gui.graph import Graph, XDef, YDef


class FitDmgVsTimeGraph(Graph):

    name = 'Damage vs Time'

    def __init__(self):
        self.eosGraphDmg = EosGraphDmg()

    @property
    def xDef(self):
        return XDef(inputDefault='0-80', inputLabel='Time (seconds)', inputIconID=1392, axisLabel='Time, s')

    @property
    def yDefs(self):
        return OrderedDict([('damage', YDef(switchLabel='Damage inflicted', axisLabel='Damage', eosGraph='eosGraphDmg'))])


FitDmgVsTimeGraph.register()
