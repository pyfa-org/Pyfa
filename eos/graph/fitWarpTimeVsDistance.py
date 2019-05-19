import math

from eos.graph import SmoothGraph


AU_METERS = 149597870700


class FitWarpTimeVsDistanceGraph(SmoothGraph):

    def getYForX(self, fit, extraData, distance):
        if distance == 0:
            return 0
        maxSubwarpSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        maxWarpSpeed = fit.warpSpeed
        time = calculate_time_in_warp(maxWarpSpeed, maxSubwarpSpeed, distance * AU_METERS)
        return time

    def _getXLimits(self, fit, extraData):
        return 0, fit.maxWarpDistance


# Taken from https://wiki.eveuniversity.org/Warp_time_calculation#Implementation
# with minor modifications
# Warp speed in AU/s, subwarp speed in m/s, distance in m
def calculate_time_in_warp(max_warp_speed, max_subwarp_speed, warp_dist):

    k_accel = max_warp_speed
    k_decel = min(max_warp_speed / 3, 2)

    warp_dropout_speed = max_subwarp_speed / 2
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
