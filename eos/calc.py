# =============================================================================
# Copyright (C) 2019 Ryan Holmes
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


# Just copy-paste penalization chain calculation code (with some modifications,
# as multipliers arrive in different form) in here to not make actual attribute
# calculations slower than they already are due to extra function calls
def calculateMultiplier(multipliers):
    """
    multipliers: dictionary in format:
    {stacking group name: [(mult, resist attr ID), (mult, resist attr ID)]}
    """
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


def calculateRangeFactor(srcOptimalRange, srcFalloffRange, distance, restrictedRange=True):
    """Range strength/chance factor, applicable to guns, ewar, RRs, etc."""
    if distance is None:
        return 1
    if srcFalloffRange > 0:
        # Most modules cannot be activated when at 3x falloff range, with few exceptions like guns
        if restrictedRange and distance > srcOptimalRange + 3 * srcFalloffRange:
            return 0
        return 0.5 ** ((max(0, distance - srcOptimalRange) / srcFalloffRange) ** 2)
    elif distance <= srcOptimalRange:
        return 1
    else:
        return 0


def calculateLockTime(srcScanRes, tgtSigRadius):
    if not srcScanRes or not tgtSigRadius:
        return None
    return min(40000 / srcScanRes / math.asinh(tgtSigRadius) ** 2, 30 * 60)
