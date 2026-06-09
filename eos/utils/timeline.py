# =============================================================================
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
# =============================================================================

import math

from eos.utils.cycles import CycleInfo, CycleSequence


class ModuleTimeline:
    """Represents repeating ON/OFF activation windows for a module."""

    def __init__(self, module, cycleParams):
        self._module = module
        self._cycleParams = cycleParams
        self._pattern = []  # list of (active_ms, inactive_ms)
        self._pattern_time = 0
        self._repeat_inf = False
        self._repeat_count = 1
        self._build_pattern()

    def _build_pattern(self):
        if self._cycleParams is None:
            return

        pulse_forced = self._module.pulseInterval is not None
        repeat_allowed = pulse_forced or not self._module.disallowRepeatingAction

        if isinstance(self._cycleParams, CycleInfo):
            active = self._cycleParams.activeTime
            inactive = self._cycleParams.inactiveTime
            quantity = self._cycleParams.quantity
            if quantity is math.inf:
                self._repeat_inf = repeat_allowed
                self._repeat_count = 1 if not repeat_allowed else math.inf
            else:
                self._repeat_count = quantity if repeat_allowed else 1
            self._pattern = [(active, inactive)]
            self._pattern_time = active + inactive
            return

        if isinstance(self._cycleParams, CycleSequence):
            # Build a single sequence pattern
            sequence_pattern = []
            for cycleInfo in self._cycleParams.sequence:
                for active, inactive, _ in cycleInfo.iterCycles():
                    sequence_pattern.append((active, inactive))
            self._pattern = sequence_pattern
            self._pattern_time = sum(active + inactive for active, inactive in sequence_pattern)
            if self._cycleParams.quantity is math.inf:
                self._repeat_inf = repeat_allowed
                self._repeat_count = 1 if not repeat_allowed else math.inf
            else:
                self._repeat_count = self._cycleParams.quantity if repeat_allowed else 1

    def is_active_at(self, timeMs):
        if timeMs is None or timeMs < 0:
            return False
        if not self._pattern:
            return True
        if self._pattern_time <= 0:
            return True

        if self._repeat_inf:
            time_in_period = timeMs % self._pattern_time
        else:
            total_time = self._pattern_time * self._repeat_count
            if timeMs >= total_time:
                return False
            time_in_period = timeMs % self._pattern_time

        cursor = 0
        for active, inactive in self._pattern:
            if time_in_period < cursor + active:
                return True
            cursor += active
            if time_in_period < cursor + inactive:
                return False
            cursor += inactive
        return False
