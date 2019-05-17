import math

from eos.graph import SmoothGraph


class FitCapAmountVsTimeGraph(SmoothGraph):

    def getYForX(self, fit, extraData, time):
        if time < 0:
            return 0
        maxCap = fit.ship.getModifiedItemAttr('capacitorCapacity')
        regenTime = fit.ship.getModifiedItemAttr('rechargeRate') / 1000
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate
        cap = maxCap * (1 + math.exp(5 * -time / regenTime) * -1) ** 2
        return cap
