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

from eos.saveddata.fit import Fit
from eos.saveddata.targetProfile import TargetProfile


def getTgtMaxVelocity(tgt, extraMultipliers=None):
    if isinstance(tgt, Fit):
        if extraMultipliers:
            maxVelocity = tgt.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=extraMultipliers)
        else:
            maxVelocity = tgt.ship.getModifiedItemAttr('maxVelocity')
    elif isinstance(tgt, TargetProfile):
        maxVelocity = tgt.maxVelocity
        if extraMultipliers:
            maxVelocity *= _calculateMultiplier(extraMultipliers)
    else:
        maxVelocity = None
    return maxVelocity


def getTgtSigRadius(tgt, extraMultipliers=None):
    if isinstance(tgt, Fit):
        if extraMultipliers:
            sigRadius = tgt.ship.getModifiedItemAttrWithExtraMods('signatureRadius', extraMultipliers=extraMultipliers)
        else:
            sigRadius = tgt.ship.getModifiedItemAttr('signatureRadius')
    elif isinstance(tgt, TargetProfile):
        sigRadius = tgt.signatureRadius
        if extraMultipliers:
            sigRadius *= _calculateMultiplier(extraMultipliers)
    else:
        sigRadius = None
    return sigRadius


def getTgtRadius(tgt):
    if isinstance(tgt, Fit):
        radius = tgt.ship.getModifiedItemAttr('radius')
    elif isinstance(tgt, TargetProfile):
        radius = tgt.radius
    else:
        radius = None
    return radius


# Just copypaste penalization chain calculation code in here to not make actual
# attribute calculations slower than it already is due to extra function calls
# Actually, with some modifications as multipliers arrive in different form
def _calculateMultiplier(multipliers):
    val = 1
    for penalizedMultipliers in multipliers.values():
        # A quick explanation of how this works:
        # 1: Bonuses and penalties are calculated seperately, so we'll have to filter each of them
        l1 = [v[0] for v in penalizedMultipliers if v[0] > 1]
        l2 = [v[0] for v in penalizedMultipliers if v[0] < 1]
        # 2: The most significant bonuses take the smallest penalty,
        # This means we'll have to sort
        abssort = lambda _val: -abs(_val - 1)
        l1.sort(key=abssort)
        l2.sort(key=abssort)
        # 3: The first module doesn't get penalized at all
        # Any module after the first takes penalties according to:
        # 1 + (multiplier - 1) * math.exp(- math.pow(i, 2) / 7.1289)
        for l in (l1, l2):
            for i in range(len(l)):
                bonus = l[i]
                val *= 1 + (bonus - 1) * math.exp(- i ** 2 / 7.1289)
    return val
