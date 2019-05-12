import math
from logbook import Logger

from eos.graph import Graph


pyfalog = Logger(__name__)


class FitCapRegenAmountGraph(Graph):

    defaults = {"percentage": '0-100'}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcRegen, data if data is not None else self.defaults)
        self.fit = fit

    def calcRegen(self, data):
        perc = data['percentage']
        maxCap = self.fit.ship.getModifiedItemAttr('capacitorCapacity')
        regenTime = self.fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        currentCap = maxCap * perc / 100
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
        regen = 10 * maxCap / regenTime * (math.sqrt(currentCap / maxCap) - currentCap / maxCap)
        return regen
