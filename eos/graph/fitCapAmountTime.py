import math
from logbook import Logger

from eos.graph import Graph


pyfalog = Logger(__name__)


class FitCapAmountTimeGraph(Graph):

    defaults = {"time": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcAmount, data if data is not None else self.defaults)
        self.fit = fit

    def calcAmount(self, data):
        time = data["time"]
        maxCap = self.fit.ship.getModifiedItemAttr('capacitorCapacity')
        regenTime = self.fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
        cap = maxCap * (1 + math.exp(5 * -time / regenTime) * -1) ** 2
        return cap
