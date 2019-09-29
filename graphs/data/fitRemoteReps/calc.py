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


from eos.calc import calculateRangeFactor
from eos.utils.float import floatUnerr
from graphs.calc import checkLockRange, checkDroneControlRange


def getApplicationPerKey(src, distance):
    inLockRange = checkLockRange(src=src, distance=distance)
    inDroneRange = checkDroneControlRange(src=src, distance=distance)
    applicationMap = {}
    for mod in src.item.activeModulesIter():
        if not mod.isRemoteRepping():
            continue
        if not inLockRange:
            applicationMap[mod] = 0
        else:
            applicationMap[mod] = calculateRangeFactor(
                srcOptimalRange=mod.maxRange or 0,
                srcFalloffRange=mod.falloff or 0,
                distance=distance)
    for drone in src.item.activeDronesIter():
        if not drone.isRemoteRepping():
            continue
        if not inLockRange or not inDroneRange:
            applicationMap[drone] = 0
        else:
            applicationMap[drone] = 1
    # Ensure consistent results - round off a little to avoid float errors
    for k, v in applicationMap.items():
        applicationMap[k] = floatUnerr(v)
    return applicationMap
