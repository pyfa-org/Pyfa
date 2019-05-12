import math
from logbook import Logger

from eos.graph import Graph


pyfalog = Logger(__name__)


class FitSpeedTimeGraph(Graph):

    defaults = {"time": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcSpeed, data if data is not None else self.defaults)
        self.fit = fit

    def calcSpeed(self, data):
        time = data["time"]
        maxSpeed = self.fit.ship.getModifiedItemAttr('maxVelocity')
        mass = self.fit.ship.getModifiedItemAttr('mass')
        agility = self.fit.ship.getModifiedItemAttr('agility')
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        speed = maxSpeed * (1 - math.exp((-time * 10 ** 6) / (agility * mass)))
        return speed
