# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import math

from eos.saveddata.fit import Fit
from eos.saveddata.targetProfile import TargetProfile


class BaseWrapper:

    def __init__(self, item):
        self.item = item

    @property
    def isFit(self):
        return isinstance(self.item, Fit)

    @property
    def isProfile(self):
        return isinstance(self.item, TargetProfile)

    @property
    def itemID(self):
        return self.item.ID

    @property
    def name(self):
        if self.isFit:
            return '{} ({})'.format(self.item.name, self.item.ship.item.name)
        elif self.isProfile:
            return self.item.name
        return ''

    @property
    def shortName(self):
        if self.isFit:
            return '{} ({})'.format(self.item.name, self.item.ship.item.getShortName())
        elif self.isProfile:
            return self.item.name
        return ''

    def getMaxVelocity(self, extraMultipliers=None):
        if self.isFit:
            if extraMultipliers:
                maxVelocity = self.item.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=extraMultipliers)
            else:
                maxVelocity = self.item.ship.getModifiedItemAttr('maxVelocity')
        elif self.isProfile:
            maxVelocity = self.item.maxVelocity
            if extraMultipliers:
                maxVelocity *= _calculateMultiplier(extraMultipliers)
        else:
            maxVelocity = None
        return maxVelocity

    def getSigRadius(self, extraMultipliers=None):
        if self.isFit:
            if extraMultipliers:
                sigRadius = self.item.ship.getModifiedItemAttrWithExtraMods('signatureRadius', extraMultipliers=extraMultipliers)
            else:
                sigRadius = self.item.ship.getModifiedItemAttr('signatureRadius')
        elif self.isProfile:
            sigRadius = self.item.signatureRadius
            if extraMultipliers:
                sigRadius *= _calculateMultiplier(extraMultipliers)
        else:
            sigRadius = None
        return sigRadius

    def getRadius(self):
        if self.isFit:
            radius = self.item.ship.getModifiedItemAttr('radius')
        elif self.isProfile:
            radius = self.item.radius
        else:
            radius = None
        return radius


class SourceWrapper(BaseWrapper):
    pass


class TargetWrapper(BaseWrapper):

    def __init__(self, item):
        super().__init__(item=item)
        self.resistMode = None


# Just copy-paste penalization chain calculation code (with some modifications,
# as multipliers arrive in different form) in here to not make actual attribute
# calculations slower than they already are due to extra function calls
def _calculateMultiplier(multipliers):
    val = 1
    for penalizedMultipliers in multipliers.values():
        # A quick explanation of how this works:
        # 1: Bonuses and penalties are calculated seperately, so we'll have to filter each of them
        l1 = [v[0] for v in penalizedMultipliers if v[0] > 1]
        l2 = [v[0] for v in penalizedMultipliers if v[0] < 1]
        # 2: The most significant bonuses take the smallest penalty,
        # This means we'll have to sort
        abssort = lambda _val: -abs(_val - 1)
        l1.sort(key=abssort)
        l2.sort(key=abssort)
        # 3: The first module doesn't get penalized at all
        # Any module after the first takes penalties according to:
        # 1 + (multiplier - 1) * math.exp(- math.pow(i, 2) / 7.1289)
        for l in (l1, l2):
            for i in range(len(l)):
                bonus = l[i]
                val *= 1 + (bonus - 1) * math.exp(- i ** 2 / 7.1289)
    return val
