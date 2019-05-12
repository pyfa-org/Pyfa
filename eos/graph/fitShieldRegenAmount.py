# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import math
from logbook import Logger

from eos.graph import Graph


pyfalog = Logger(__name__)


class FitShieldRegenAmountGraph(Graph):

    defaults = {"percentage": '0-100'}

    def __init__(self, fit, data=None):
        Graph.__init__(self, fit, self.calcRegen, data if data is not None else self.defaults)
        self.fit = fit
        import gui.mainFrame
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def calcRegen(self, data):
        perc = data["percentage"]
        maxShield = self.fit.ship.getModifiedItemAttr('shieldCapacity')
        regenTime = self.fit.ship.getModifiedItemAttr('shieldRechargeRate') / 1000
        currentShield = maxShield * perc / 100
        regen = 10 * maxShield / regenTime * (math.sqrt(currentShield / maxShield) - currentShield / maxShield)
        useEhp = self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
        if self.fit.damagePattern is not None and useEhp:
            regen = self.fit.damagePattern.effectivify(self.fit, regen, 'shield')
        return regen
