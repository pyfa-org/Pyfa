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


import math
from collections import namedtuple

from eos.const import SpoolType
from eos.utils.float import floatUnerr


SpoolOptions = namedtuple('SpoolOptions', ('spoolType', 'spoolAmount', 'force'))


def calculateSpoolup(modMaxValue, modStepValue, modCycleTime, spoolType, spoolAmount):
    """
    Calculate damage multiplier increment based on passed parameters. Module cycle time
    is specified in seconds.

    Returns spoolup value, amount of cycles to reach it and time to reach it.
    """
    if not modMaxValue or not modStepValue:
        return 0, 0, 0
    if spoolType == SpoolType.SPOOL_SCALE:
        # Find out at which point of spoolup scale we're on, find out how many cycles
        # is enough to reach it and recalculate spoolup value for that amount of cycles
        cycles = math.ceil(floatUnerr(modMaxValue * spoolAmount / modStepValue))
        spoolValue = min(modMaxValue, cycles * modStepValue)
        return spoolValue, cycles, cycles * modCycleTime
    elif spoolType == SpoolType.CYCLE_SCALE:
        # For cycle scale, find out max amount of cycles and scale against it
        cycles = round(spoolAmount * math.ceil(floatUnerr(modMaxValue / modStepValue)))
        spoolValue = min(modMaxValue, cycles * modStepValue)
        return spoolValue, cycles, cycles * modCycleTime
    elif spoolType == SpoolType.TIME:
        cycles = min(
            # How many full cycles mod had by passed time
            math.floor(floatUnerr(spoolAmount / modCycleTime)),
            # Max amount of cycles
            math.ceil(floatUnerr(modMaxValue / modStepValue)))
        spoolValue = min(modMaxValue, cycles * modStepValue)
        return spoolValue, cycles, cycles * modCycleTime
    elif spoolType == SpoolType.CYCLES:
        cycles = min(
            # Consider full cycles only
            math.floor(spoolAmount),
            # Max amount of cycles
            math.ceil(floatUnerr(modMaxValue / modStepValue)))
        spoolValue = min(modMaxValue, cycles * modStepValue)
        return spoolValue, cycles, cycles * modCycleTime
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
