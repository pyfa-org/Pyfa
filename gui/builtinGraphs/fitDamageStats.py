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

from eos.graph.fitDpsVsRange import FitDpsVsRangeGraph as EosGraph
from .base import Graph, XDef, YDef, Input


class FitDamageStatsGraph(Graph):

    name = 'Damage Stats'

    def __init__(self):
        super().__init__()
        self.eosGraph = EosGraph()

    @property
    def xDefs(self):
        return XDef(inputDefault='0-100', inputLabel='Distance to target (km)', inputIconID=1391, axisLabel='Distance to target, km')

    @property
    def yDefs(self):
        return OrderedDict([('dps', YDef(switchLabel='DPS', axisLabel='DPS', eosGraph='eosGraph'))])

    @property
    def inputs(self):
        return OrderedDict([
            ('time', Input(handle='time', label='Time', unit='s', iconID=1392, defaultValue=None, defaultRange=(0, 80))),
            ('atkSpeed', Input(handle='atkSpeed', label=None, unit=None, iconID=None, defaultValue=None, defaultRange=None)),
            ('atkAngle', Input(handle='atkAngle', label=None, unit=None, iconID=None, defaultValue=None, defaultRange=None)),
            ('tgtSpeed', Input(handle='tgtSpeed', label='Target speed', unit='%', iconID=1389, defaultValue=100, defaultRange=(0, 100))),
            ('tgtAngle', Input(handle='tgtAngle', label=None, unit=None, iconID=None, defaultValue=None, defaultRange=None)),
            ('tgtSigRad', Input(handle='tgtSigRad', label='Target signature radius', unit='%', iconID=1390, defaultValue=100, defaultRange=(100, 200)))])

    @property
    def hasTargets(self):
        return True

    @property
    def hasVectors(self):
        return True


FitDamageStatsGraph.register()
