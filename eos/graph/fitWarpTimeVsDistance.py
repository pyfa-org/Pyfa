import math

from eos.const import FittingModuleState
from eos.graph import SmoothGraph


AU_METERS = 149597870700


class FitWarpTimeVsDistanceGraph(SmoothGraph):

    def __init__(self):
        super().__init__()
        self.subwarpSpeed = None

    def getYForX(self, fit, extraData, distance):
        if distance == 0:
            return 0
        if fit.ID not in self.cache:
            self.__generateCache(fit)
        maxWarpSpeed = fit.warpSpeed
        subwarpSpeed = self.cache[fit.ID]['cleanSubwarpSpeed']
        time = calculate_time_in_warp(maxWarpSpeed, subwarpSpeed, distance * AU_METERS)
        return time

    def _getXLimits(self, fit, extraData):
        return 0, fit.maxWarpDistance

    def __generateCache(self, fit):
        modStates = {}
        for mod in fit.modules:
            if mod.item is not None and mod.item.group.name in ('Propulsion Module', 'Mass Entanglers', 'Cloaking Device') and mod.state >= FittingModuleState.ACTIVE:
                modStates[mod] = mod.state
                mod.state = FittingModuleState.ONLINE
        projFitStates = {}
        for projFit in fit.projectedFits:
            projectionInfo = projFit.getProjectionInfo(fit.ID)
            if projectionInfo is not None and projectionInfo.active:
                projFitStates[projectionInfo] = projectionInfo.active
                projectionInfo.active = False
        projModStates = {}
        for mod in fit.projectedModules:
            if not mod.isExclusiveSystemEffect and mod.state >= FittingModuleState.ACTIVE:
                projModStates[mod] = mod.state
                mod.state = FittingModuleState.ONLINE
        projDroneStates = {}
        for drone in fit.projectedDrones:
            if drone.amountActive > 0:
                projDroneStates[drone] = drone.amountActive
                drone.amountActive = 0
        projFighterStates = {}
        for fighter in fit.projectedFighters:
            if fighter.active:
                projFighterStates[fighter] = fighter.active
                fighter.active = False
        fit.calculateModifiedAttributes()
        self.cache[fit.ID] = {'cleanSubwarpSpeed': fit.ship.getModifiedItemAttr('maxVelocity')}
        for projInfo, state in projFitStates.items():
            projInfo.active = state
        for mod, state in modStates.items():
            mod.state = state
        for mod, state in projModStates.items():
            mod.state = state
        for drone, amountActive in projDroneStates.items():
            drone.amountActive = amountActive
        for fighter, state in projFighterStates.items():
            fighter.active = state
        fit.calculateModifiedAttributes()


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
