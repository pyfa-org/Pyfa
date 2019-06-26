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


import math

from eos.graph.fitDpsVsRange import FitDpsVsRangeGraph as EosGraph
from .base import Graph, XDef, YDef, Input, VectorDef


class FitDamageStatsGraph(Graph):

    name = 'Damage Stats'

    def __init__(self):
        super().__init__()
        self.eosGraph = EosGraph()

    @property
    def xDefs(self):
        return [
            XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km')),
            XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
            XDef(handle='tgtSpeed', unit='m/s', label='Target speed', mainInput=('tgtSpeed', '%')),
            XDef(handle='tgtSpeed', unit='%', label='Target speed', mainInput=('tgtSpeed', '%')),
            XDef(handle='tgtSigRad', unit='m', label='Target signature radius', mainInput=('tgtSigRad', '%')),
            XDef(handle='tgtSigRad', unit='%', label='Target signature radius', mainInput=('tgtSigRad', '%'))]

    @property
    def yDefs(self):
        return [
            YDef(handle='dps', unit=None, label='DPS', eosGraph='eosGraph'),
            YDef(handle='volley', unit=None, label='Volley', eosGraph='eosGraph'),
            YDef(handle='damage', unit=None, label='Damage inflicted', eosGraph='eosGraph')]

    @property
    def inputs(self):
        return [
            Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=None, defaultRange=(0, 80), mainOnly=False),
            Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=50, defaultRange=(0, 100), mainOnly=False),
            Input(handle='tgtSpeed', unit='%', label='Target speed', iconID=1389, defaultValue=100, defaultRange=(0, 100), mainOnly=False),
            Input(handle='tgtSigRad', unit='%', label='Target signature', iconID=1390, defaultValue=100, defaultRange=(100, 200), mainOnly=True)]

    @property
    def srcVectorDef(self):
        return VectorDef(lengthHandle='atkSpeed', lengthUnit='%', angleHandle='atkAngle', angleUnit='degrees', label='Attacker')

    @property
    def tgtVectorDef(self):
        return VectorDef(lengthHandle='tgtSpeed', lengthUnit='%', angleHandle='tgtAngle', angleUnit='degrees', label='Target')

    @property
    def hasTargets(self):
        return True


FitDamageStatsGraph.register()
