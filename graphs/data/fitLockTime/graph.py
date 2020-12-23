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

import wx

from graphs.data.base import FitGraph, Input, XDef, YDef
from .getter import TgtSigRadius2LockTimeGetter

_t = wx.GetTranslation


class FitLockTimeGraph(FitGraph):
    # UI stuff
    internalName = 'lockTimeGraph'
    name = _t('Lock Time')
    xDefs = [XDef(handle='tgtSigRad', unit='m', label=_t('Target signature radius'), mainInput=('tgtSigRad', 'm'))]
    yDefs = [YDef(handle='time', unit='s', label=_t('Lock time'))]
    inputs = [Input(handle='tgtSigRad', unit='m', label=_t('Target signature'), iconID=1390, defaultValue=None, defaultRange=(25, 500))]
    srcExtraCols = ('ScanResolution',)

    # Calculation stuff
    _limiters = {'tgtSigRad': lambda src, tgt: (1, math.inf)}
    _getters = {('tgtSigRad', 'time'): TgtSigRadius2LockTimeGetter}
