import math

from eos.graph import SmoothGraph


class FitDistanceVsTimeGraph(SmoothGraph):

    def getYForX(self, fit, extraData, time):
        maxSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        mass = fit.ship.getModifiedItemAttr('mass')
        agility = fit.ship.getModifiedItemAttr('agility')
        # Definite integral of:
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        distance_t = maxSpeed * time + (maxSpeed * agility * mass * math.exp((-time * 1000000) / (agility * mass)) / 1000000)
        distance_0 = maxSpeed * 0 + (maxSpeed * agility * mass * math.exp((-0 * 1000000) / (agility * mass)) / 1000000)
        distance = distance_t - distance_0
        return distance
