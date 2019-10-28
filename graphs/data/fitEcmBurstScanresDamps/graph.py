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


"""
Disclaimer by kadesh: this graph was made to analyze my ECM burst + damp frig
concept. I do not think it is useful for regular player, so it is disabled.
Enable by setting config.experimentalFeatures = True.
"""


import math

from graphs.data.base import FitGraph, XDef, YDef, Input, InputCheckbox
from .getter import (
    TgtScanRes2TgtLockTimeGetter, TgtScanRes2TgtLockUptimeGetter,
    TgtScanRes2SrcDmgGetter, TgtDps2SrcDmgGetter)


class FitEcmBurstScanresDampsGraph(FitGraph):

    # UI stuff
    hidden = True
    internalName = 'ecmBurstScanresDamps'
    name = 'ECM Burst + Scanres Damps'
    xDefs = [
        XDef(handle='tgtDps', unit=None, label='Enemy DPS', mainInput=('tgtDps', None)),
        XDef(handle='tgtScanRes', unit='mm', label='Enemy scanres', mainInput=('tgtScanRes', 'mm'))]
    yDefs = [
        YDef(handle='srcDmg', unit=None, label='Damage inflicted'),
        YDef(handle='tgtLockTime', unit='s', label='Lock time'),
        YDef(handle='tgtLockUptime', unit='s', label='Lock uptime')]
    inputs = [
        Input(handle='tgtScanRes', unit='mm', label='Enemy scanres', iconID=74, defaultValue=700, defaultRange=(100, 1000)),
        Input(handle='tgtDps', unit=None, label='Enemy DPS', iconID=1432, defaultValue=200, defaultRange=(100, 600)),
        Input(handle='uptimeAdj', unit='s', label='Uptime adjustment', iconID=1392, defaultValue=1, defaultRange=(None, None), conditions=[(None, ('srcDmg', None))]),
        Input(handle='uptimeAmtLimit', unit=None, label='Max amount of uptimes', iconID=1397, defaultValue=3, defaultRange=(None, None), conditions=[(None, ('srcDmg', None))])]
    checkboxes = [
        InputCheckbox(handle='applyDamps', label='Apply sensor dampeners', defaultValue=True),
        InputCheckbox(handle='applyDrones', label='Use drones', defaultValue=True, conditions=[(None, ('srcDmg', None))])]
    srcExtraCols = ('SigRadius', 'Damp ScanRes')

    # Calculation stuff
    _limiters = {'tgtScanRes': lambda src, tgt: (1, math.inf)}
    _getters = {
        ('tgtScanRes', 'tgtLockTime'): TgtScanRes2TgtLockTimeGetter,
        ('tgtScanRes', 'tgtLockUptime'): TgtScanRes2TgtLockUptimeGetter,
        ('tgtScanRes', 'srcDmg'): TgtScanRes2SrcDmgGetter,
        ('tgtDps', 'srcDmg'): TgtDps2SrcDmgGetter}
