import math

from eos.graph import SmoothGraph


class FitCapRegenVsCapPercGraph(SmoothGraph):

    def getYForX(self, fit, extraData, perc):
        maxCap = fit.ship.getModifiedItemAttr('capacitorCapacity')
        regenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        currentCap = maxCap * perc / 100
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
        regen = 10 * maxCap / regenTime * (math.sqrt(currentCap / maxCap) - currentCap / maxCap)
        return regen
