import math
from logbook import Logger

from eos.graph import Graph


pyfalog = Logger(__name__)


class FitShieldAmountTimeGraph(Graph):

    defaults = {"time": 0}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcAmount, data if data is not None else self.defaults)
        self.fit = fit
        import gui.mainFrame
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def calcAmount(self, data):
        time = data["time"]
        maxShield = self.fit.ship.getModifiedItemAttr('shieldCapacity')
        regenTime = self.fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate (shield is similar to cap)
        shield = maxShield * (1 + math.exp(5 * -time / regenTime) * -1) ** 2
        useEhp = self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
        if self.fit.damagePattern is not None and useEhp:
            shield = self.fit.damagePattern.effectivify(self.fit, shield, 'shield')
        return shield
