import math

from eos.graph import SmoothGraph


class FitShieldRegenVsShieldPercGraph(SmoothGraph):

    def __init__(self):
        super().__init__()
        import gui.mainFrame
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getYForX(self, fit, extraData, perc):
        maxShield = fit.ship.getModifiedItemAttr('shieldCapacity')
        regenTime = fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        currentShield = maxShield * perc / 100
        # https://wiki.eveuniversity.org/Capacitor#Capacitor_recharge_rate (shield is similar to cap)
        regen = 10 * maxShield / regenTime * (math.sqrt(currentShield / maxShield) - currentShield / maxShield)
        useEhp = self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
        if fit.damagePattern is not None and useEhp:
            regen = fit.damagePattern.effectivify(fit, regen, 'shield')
        return regen
