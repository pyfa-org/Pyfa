import math
from logbook import Logger

from .base import SmoothGraph


pyfalog = Logger(__name__)


class FitShieldAmountVsTimeGraph(SmoothGraph):

    def __init__(self):
        super().__init__()
        import gui.mainFrame
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getYForX(self, fit, extraData, time):
        if time < 0:
            return 0
        maxShield = fit.ship.getModifiedItemAttr('shieldCapacity')
        regenTime = fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate (shield is similar to cap)
        shield = maxShield * (1 + math.exp(5 * -time / regenTime) * -1) ** 2
        useEhp = self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
        if fit.damagePattern is not None and useEhp:
            shield = fit.damagePattern.effectivify(fit, shield, 'shield')
        return shield
