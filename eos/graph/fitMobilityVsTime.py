import math

from eos.graph import Graph


class FitMobilityVsTimeGraph(Graph):

    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        xs = []
        ysSpeed = []
        ysDistance = []
        for x in self._xIter(xRange, xAmount):
            xs.append(x)
            ysSpeed.append(self.calcSpeed(fit, x))
            ysDistance.append(self.calcDistance(fit, x))
        return xs, {'speed': ysSpeed, 'distance': ysDistance}

    def getYForX(self, fit, extraData, x):
        return {'speed': self.calcSpeed(fit, x), 'distance': self.calcDistance(fit, x)}

    @staticmethod
    def calcSpeed(fit, time):
        maxSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        mass = fit.ship.getModifiedItemAttr('mass')
        agility = fit.ship.getModifiedItemAttr('agility')
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        speed = maxSpeed * (1 - math.exp((-time * 1000000) / (agility * mass)))
        return speed

    @staticmethod
    def calcDistance(fit, time):
        maxSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
        mass = fit.ship.getModifiedItemAttr('mass')
        agility = fit.ship.getModifiedItemAttr('agility')
        # Definite integral of:
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        distance_t = maxSpeed * time + (maxSpeed * agility * mass * math.exp((-time * 1000000) / (agility * mass)) / 1000000)
        distance_0 = maxSpeed * 0 + (maxSpeed * agility * mass * math.exp((-0 * 1000000) / (agility * mass)) / 1000000)
        distance = distance_t - distance_0
        return distance
