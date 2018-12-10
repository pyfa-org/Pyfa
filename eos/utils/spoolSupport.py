# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================


from enum import IntEnum, unique

from eos.utils.float import floatUnerr


@unique
class SpoolType(IntEnum):
    SCALE = 0  #  [0..1]
    TIME = 1  # Expressed via time in seconds since spoolup started
    CYCLES = 2  # Expressed in amount of cycles since spoolup started


def calculateSpoolup(modMaxValue, modStepValue, modCycleTime, spoolType, spoolAmount):
    if spoolType == SpoolType.SCALE:
        return int(floatUnerr(spoolAmount * modMaxValue / modStepValue)) * modStepValue
    elif spoolType == SpoolType.TIME:
        cycles = int(floatUnerr(spoolAmount / modCycleTime))
        return min(modMaxValue, cycles * modStepValue)
    elif spoolType == SpoolType.CYCLES:
        cycles = int(spoolAmount)
        return min(modMaxValue, cycles * modStepValue)
    else:
        return 0
