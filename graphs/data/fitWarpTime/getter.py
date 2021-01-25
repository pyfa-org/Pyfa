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

from graphs.data.base import SmoothPointGetter


AU_METERS = 149597870700


class Distance2TimeGetter(SmoothPointGetter):

    _baseResolution = 500

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'subwarpSpeed': self.graph._subspeedCache.getSubwarpSpeed(src),
            'warpSpeed': src.item.warpSpeed}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        time = calculate_time_in_warp(
            max_subwarp_speed=commonData['subwarpSpeed'],
            max_warp_speed=commonData['warpSpeed'],
            warp_dist=distance)
        return time


# Taken from https://wiki.eveuniversity.org/Warp_time_calculation#Implementation
# with minor modifications
# Warp speed in AU/s, subwarp speed in m/s, distance in m
def calculate_time_in_warp(max_warp_speed, max_subwarp_speed, warp_dist):

    if warp_dist == 0:
        return 0

    k_accel = max_warp_speed
    k_decel = min(max_warp_speed / 3, 2)

    warp_dropout_speed = min(max_subwarp_speed / 2, 100)
    max_ms_warp_speed = max_warp_speed * AU_METERS

    accel_dist = AU_METERS
    decel_dist = max_ms_warp_speed / k_decel

    minimum_dist = accel_dist + decel_dist

    cruise_time = 0

    if minimum_dist > warp_dist:
        max_ms_warp_speed = warp_dist * k_accel * k_decel / (k_accel + k_decel)
    else:
        cruise_time = (warp_dist - minimum_dist) / max_ms_warp_speed

    accel_time = math.log(max_ms_warp_speed / k_accel) / k_accel
    decel_time = math.log(max_ms_warp_speed / warp_dropout_speed) / k_decel

    total_time = cruise_time + accel_time + decel_time
    return total_time
