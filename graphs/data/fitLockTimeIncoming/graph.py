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

from graphs.data.base import FitGraph, XDef, YDef, Input, InputCheckbox
from .getter import ScanRes2LockTimeGetter


class FitLockTimeIncomingGraph(FitGraph):

    # UI stuff
    internalName = 'lockTimeIncomingGraph'
    name = 'Lock Time (Incoming)'
    xDefs = [XDef(handle='scanRes', unit='mm', label='Scan resolution', mainInput=('scanRes', 'mm'))]
    yDefs = [YDef(handle='time', unit='s', label='Lock time')]
    inputs = [Input(handle='scanRes', unit='mm', label='Scan resolution', iconID=74, defaultValue=None, defaultRange=(100, 1000))]
    checkboxes = [InputCheckbox(handle='applyDamps', label='Apply sensor dampeners', defaultValue=True)]
    srcExtraCols = ('SigRadius', 'Damp ScanRes')

    # Calculation stuff
    _limiters = {'scanRes': lambda src, tgt: (1, math.inf)}
    _getters = {('scanRes', 'time'): ScanRes2LockTimeGetter}
