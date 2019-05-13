import math
from logbook import Logger

from eos.graph import Graph


pyfalog = Logger(__name__)


class FitDistanceTimeGraph(Graph):

    defaults = {"time": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcDistance, data if data is not None else self.defaults)
        self.fit = fit

    def calcDistance(self, data):
        time = data["time"]
        maxSpeed = self.fit.ship.getModifiedItemAttr('maxVelocity')
        mass = self.fit.ship.getModifiedItemAttr('mass')
        agility = self.fit.ship.getModifiedItemAttr('agility')
        # Definite integral of:
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        distance_t = maxSpeed * time + (maxSpeed * agility * mass * math.exp((-time * 1000000) / (agility * mass)) / 1000000)
        distance_0 = maxSpeed * 0 + (maxSpeed * agility * mass * math.exp((-0 * 1000000) / (agility * mass)) / 1000000)
        distance = distance_t - distance_0
        return distance
