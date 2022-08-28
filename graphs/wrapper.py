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


from eos.calc import calculateMultiplier
from eos.saveddata.damagePattern import DamagePattern
from eos.saveddata.fit import Fit
from eos.saveddata.targetProfile import TargetProfile
from service.const import TargetResistMode


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
    def name(self):
        if self.isFit:
            return '{} ({})'.format(self.item.name, self.item.ship.item.name)
        elif self.isProfile:
            return self.item.fullName
        return ''

    @property
    def shortName(self):
        if self.isFit:
            return '{} ({})'.format(self.item.name, self.item.ship.item.getShortName())
        elif self.isProfile:
            return self.item.shortName
        return ''

    def getMaxVelocity(self, extraMultipliers=None, ignoreAfflictors=()):
        if self.isFit:
            if extraMultipliers or ignoreAfflictors:
                maxVelocity = self.item.ship.getModifiedItemAttrExtended(
                    'maxVelocity',
                    extraMultipliers=extraMultipliers,
                    ignoreAfflictors=ignoreAfflictors)
            else:
                maxVelocity = self.item.ship.getModifiedItemAttr('maxVelocity')
        elif self.isProfile:
            maxVelocity = self.item.maxVelocity
            if extraMultipliers:
                maxVelocity *= calculateMultiplier(extraMultipliers)
        else:
            maxVelocity = None
        return maxVelocity

    def getSigRadius(self, extraMultipliers=None, ignoreAfflictors=()):
        if self.isFit:
            if extraMultipliers or ignoreAfflictors:
                sigRadius = self.item.ship.getModifiedItemAttrExtended(
                    'signatureRadius',
                    extraMultipliers=extraMultipliers,
                    ignoreAfflictors=ignoreAfflictors)
            else:
                sigRadius = self.item.ship.getModifiedItemAttr('signatureRadius')
        elif self.isProfile:
            sigRadius = self.item.signatureRadius
            if extraMultipliers:
                sigRadius *= calculateMultiplier(extraMultipliers)
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

    def __init__(self, item, colorID):
        super().__init__(item)
        self._colorID = colorID

    @property
    def colorID(self):
        return self._colorID

    @colorID.setter
    def colorID(self, value):
        self._colorID = value


class TargetWrapper(BaseWrapper):

    def __init__(self, item, lightnessID, lineStyleID):
        super().__init__(item=item)
        self.lightnessID = lightnessID
        self.lineStyleID = lineStyleID
        self.resistMode = TargetResistMode.auto

    def getResists(self, includeLayer=False):
        em = therm = kin = explo = 0
        layer = None
        if self.isProfile:
            em = self.item.emAmount
            therm = self.item.thermalAmount
            kin = self.item.kineticAmount
            explo = self.item.explosiveAmount
        if self.isFit:
            if self.resistMode == TargetResistMode.auto:
                em, therm, kin, explo, layer = _getAutoResists(fit=self.item)
            elif self.resistMode == TargetResistMode.shield:
                em, therm, kin, explo = _getShieldResists(ship=self.item.ship)
            elif self.resistMode == TargetResistMode.armor:
                em, therm, kin, explo = _getArmorResists(ship=self.item.ship)
            elif self.resistMode == TargetResistMode.hull:
                em, therm, kin, explo = _getHullResists(ship=self.item.ship)
            elif self.resistMode == TargetResistMode.weightedAverage:
                em, therm, kin, explo = _getWeightedResists(fit=self.item)
        if includeLayer:
            return em, therm, kin, explo, layer
        else:
            return em, therm, kin, explo



def _getShieldResists(ship):
    em = 1 - ship.getModifiedItemAttr('shieldEmDamageResonance')
    therm = 1 - ship.getModifiedItemAttr('shieldThermalDamageResonance')
    kin = 1 - ship.getModifiedItemAttr('shieldKineticDamageResonance')
    explo = 1 - ship.getModifiedItemAttr('shieldExplosiveDamageResonance')
    return em, therm, kin, explo


def _getArmorResists(ship):
    em = 1 - ship.getModifiedItemAttr('armorEmDamageResonance')
    therm = 1 - ship.getModifiedItemAttr('armorThermalDamageResonance')
    kin = 1 - ship.getModifiedItemAttr('armorKineticDamageResonance')
    explo = 1 - ship.getModifiedItemAttr('armorExplosiveDamageResonance')
    return em, therm, kin, explo


def _getHullResists(ship):
    em = 1 - ship.getModifiedItemAttr('emDamageResonance')
    therm = 1 - ship.getModifiedItemAttr('thermalDamageResonance')
    kin = 1 - ship.getModifiedItemAttr('kineticDamageResonance')
    explo = 1 - ship.getModifiedItemAttr('explosiveDamageResonance')
    return em, therm, kin, explo


def _getWeightedResists(fit):
    shieldEmRes, shieldThermRes, shieldKinRes, shieldExploRes = _getShieldResists(fit.ship)
    armorEmRes, armorThermRes, armorKinRes, armorExploRes = _getArmorResists(fit.ship)
    hullEmRes, hullThermRes, hullKinRes, hullExploRes = _getHullResists(fit.ship)
    hpData = fit.hp
    shieldHp = hpData['shield']
    armorHp = hpData['armor']
    hullHp = hpData['hull']
    totalHp = shieldHp + armorHp + hullHp
    totalEhpEm = shieldHp / (1 - shieldEmRes) + armorHp / (1 - armorEmRes) + hullHp / (1 - hullEmRes)
    totalEhpTherm = shieldHp / (1 - shieldThermRes) + armorHp / (1 - armorThermRes) + hullHp / (1 - hullThermRes)
    totalEhpKin = shieldHp / (1 - shieldKinRes) + armorHp / (1 - armorKinRes) + hullHp / (1 - hullKinRes)
    totalEhpExplo = shieldHp / (1 - shieldExploRes) + armorHp / (1 - armorExploRes) + hullHp / (1 - hullExploRes)
    weightedEmRes = 1 - totalHp / totalEhpEm
    weightedThermRes = 1 - totalHp / totalEhpTherm
    weightedKinRes = 1 - totalHp / totalEhpKin
    weightedExploRes = 1 - totalHp / totalEhpExplo
    return weightedEmRes, weightedThermRes, weightedKinRes, weightedExploRes


def _getAutoResists(fit):
    # Get all the data
    # HP / EHP
    hpData = fit.hp
    shieldHp = hpData['shield']
    armorHp = hpData['armor']
    hullHp = hpData['hull']
    uniformDamagePattern = DamagePattern(emAmount=25, thermalAmount=25, kineticAmount=25, explosiveAmount=25)
    ehpData = uniformDamagePattern.calculateEhp(fit.ship)
    shieldEhp = ehpData['shield']
    armorEhp = ehpData['armor']
    hullEhp = ehpData['hull']
    totalEhp = shieldEhp + armorEhp + hullEhp
    # Resist factors
    try:
        shieldResFactor = shieldEhp / shieldHp
    except ZeroDivisionError:
        shieldResFactor = 1
    try:
        armorResFactor = armorEhp / armorHp
    except ZeroDivisionError:
        armorResFactor = 1
    try:
        hullResFactor = hullEhp / hullHp
    except ZeroDivisionError:
        hullResFactor = 1
    # Tank
    tankData = fit.tank
    shieldTank = tankData['shieldRepair']
    armorTank = tankData['armorRepair']
    hullTank = tankData['hullRepair']
    shieldRegen = tankData['passiveShield']

    shieldScore = 0
    armorScore = 0
    hullScore = 0
    # EHP scoring
    ehpWeight = 100
    shieldScore += ehpWeight * (shieldEhp / totalEhp) ** 1.5
    armorScore += ehpWeight * (armorEhp / totalEhp) ** 1.5
    hullScore += ehpWeight * (hullEhp / totalEhp) ** 1.5
    # Resists scoring
    # We include it to have some extra points for receiving better reps from the outside
    resistWeight = 25
    bestResFactor = max(shieldResFactor, armorResFactor, hullResFactor)
    shieldScore += resistWeight * (shieldResFactor / bestResFactor) ** 1.5
    armorScore += resistWeight * (armorResFactor / bestResFactor) ** 1.5
    hullScore += resistWeight * (hullResFactor / bestResFactor) ** 1.5
    # Active tank
    activeWeight = 10000
    shieldScore += activeWeight * shieldTank * shieldResFactor / totalEhp
    armorScore += activeWeight * armorTank * armorResFactor / totalEhp
    hullScore += activeWeight * hullTank * hullResFactor / totalEhp
    # Shield regen
    regenWeight = 5000
    shieldScore += regenWeight * shieldRegen * shieldResFactor / totalEhp
    maxScore = max(shieldScore, armorScore, hullScore)
    if maxScore == shieldScore:
        return (*_getShieldResists(fit.ship), 'shield')
    if maxScore == armorScore:
        return (*_getArmorResists(fit.ship), 'armor')
    if maxScore == hullScore:
        return (*_getHullResists(fit.ship), 'hull')
    return 0, 0, 0, 0, None
