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


from collections import namedtuple
from enum import IntEnum, unique

from eos.utils.float import floatUnerr


SpoolOptions = namedtuple('SpoolOptions', ('spoolType', 'spoolAmount', 'force'))


@unique
class SpoolType(IntEnum):
    SCALE = 0  # [0..1]
    TIME = 1  # Expressed via time in seconds since spool up started
    CYCLES = 2  # Expressed in amount of cycles since spool up started


def calculateSpoolup(modMaxValue, modStepValue, modCycleTime, spoolType, spoolAmount):
    """
    Calculate damage multiplier increment based on passed parameters. Module cycle time
    is specified in seconds.

    Returns spoolup value, amount of cycles to reach it and time to reach it.
    """
    if not modMaxValue or not modStepValue:
        return 0, 0, 0
    if spoolType == SpoolType.SCALE:
        cycles = int(floatUnerr(spoolAmount * modMaxValue / modStepValue))
        return cycles * modStepValue, cycles, cycles * modCycleTime
    elif spoolType == SpoolType.TIME:
        cycles = min(int(floatUnerr(spoolAmount / modCycleTime)), int(floatUnerr(modMaxValue / modStepValue)))
        return cycles * modStepValue, cycles, cycles * modCycleTime
    elif spoolType == SpoolType.CYCLES:
        cycles = min(int(spoolAmount), int(floatUnerr(modMaxValue / modStepValue)))
        return cycles * modStepValue, cycles, cycles * modCycleTime
    else:
        return 0, 0, 0


def resolveSpoolOptions(spoolOptions, module):
    # Rely on passed options if they are forcing us to do so
    if spoolOptions is not None and spoolOptions.force:
        return spoolOptions.spoolType, spoolOptions.spoolAmount
    # If we're not forced to use options and module has options set, prefer on-module values
    elif module is not None and module.spoolType is not None:
        return module.spoolType, module.spoolAmount
    # Otherwise - rely on passed options
    elif spoolOptions is not None:
        return spoolOptions.spoolType, spoolOptions.spoolAmount
    else:
        return None, None
