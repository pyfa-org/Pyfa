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
