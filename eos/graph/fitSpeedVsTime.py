import math

from .base import SmoothGraph


class FitSpeedVsTimeGraph(SmoothGraph):

    def getYForX(self, fit, extraData, time):
        maxSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        mass = fit.ship.getModifiedItemAttr('mass')
        agility = fit.ship.getModifiedItemAttr('agility')
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        speed = maxSpeed * (1 - math.exp((-time * 1000000) / (agility * mass)))
        return speed
