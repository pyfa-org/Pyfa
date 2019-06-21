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
        return OrderedDict([
            ('distance', XDef(handle='distance', label='Distance', unit='km', mainInputHandle='distance')),
            ('time', XDef(handle='time', label='Time', unit='s', mainInputHandle='time')),
            ('tgtSpeedAbs', XDef(handle='tgtSpeedAbs', label='Target speed', unit='m/s', mainInputHandle='tgtSpeed')),
            ('tgtSpeedRel', XDef(handle='tgtSpeedRel', label='Target speed', unit='%', mainInputHandle='tgtSpeed')),
            ('tgtSigRadAbs', XDef(handle='tgtSigRadAbs', label='Target signature radius', unit='m', mainInputHandle='tgtSigRad')),
            ('tgtSigRadRel', XDef(handle='tgtSigRadRel', label='Target signature radius', unit='%', mainInputHandle='tgtSigRad'))])

    @property
    def yDefs(self):
        return OrderedDict([
            ('dps', YDef(handle='dps', label='DPS', unit=None, eosGraph='eosGraph')),
            ('volley', YDef(handle='volley', label='Volley', unit=None, eosGraph='eosGraph')),
            ('damage', YDef(handle='damage', label='Damage inflicted', unit=None, eosGraph='eosGraph'))])

    @property
    def inputs(self):
        return OrderedDict([
            ('time', Input(handle='time', label='Time', unit='s', iconID=1392, defaultValue=None, defaultRange=(0, 80))),
            ('distance', Input(handle='distance', label='Distance', unit='km', iconID=1391, defaultValue=50, defaultRange=(0, 100))),
            ('tgtSpeed', Input(handle='tgtSpeed', label='Target speed', unit='%', iconID=1389, defaultValue=100, defaultRange=(0, 100))),
            ('tgtSigRad', Input(handle='tgtSigRad', label='Target signature radius', unit='%', iconID=1390, defaultValue=100, defaultRange=(100, 200)))])

    @property
    def hasTargets(self):
        return True

    @property
    def hasSrcVector(self):
        return True

    @property
    def srcVectorLengthHandle(self):
        return 'atkSpeed'

    @property
    def srcVectorAngleHandle(self):
        return 'atkAngle'

    @property
    def hasTgtVector(self):
        return True

    @property
    def tgtVectorLengthHandle(self):
        return 'tgtSpeed'

    @property
    def tgtVectorAngleHandle(self):
        return 'tgtAngle'


FitDamageStatsGraph.register()
