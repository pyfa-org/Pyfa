import math

from eos.graph import Graph


class FitCapRegenVsCapPercGraph(Graph):

    def getPlotPoints(self, fit, extraData, xRange, xAmount):
        xs = []
        ys = []
        for x in self._xIter(xRange, xAmount):
            xs.append(x)
            ys.append(self.calc(fit, x))
        return xs, {'capRegen': ys}

    def getYForX(self, fit, extraData, x):
        return {'capRegen': self.calc(fit, x)}

    @staticmethod
    def calc(fit, perc):
        maxCap = fit.ship.getModifiedItemAttr('capacitorCapacity')
        regenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        currentCap = maxCap * perc / 100
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
        regen = 10 * maxCap / regenTime * (math.sqrt(currentCap / maxCap) - currentCap / maxCap)
        return regen
