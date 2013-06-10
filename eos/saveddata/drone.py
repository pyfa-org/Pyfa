#===============================================================================
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
#===============================================================================

from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut, ChargeAttrShortcut
from eos.effectHandlerHelpers import HandledItem, HandledCharge
from sqlalchemy.orm import validates, reconstructor

class Drone(HandledItem, HandledCharge, ItemAttrShortcut, ChargeAttrShortcut):
    DAMAGE_ATTRIBUTES = ("emDamage", "kineticDamage", "explosiveDamage", "thermalDamage")

    def __init__(self, item):
        if item.category.name != "Drone":
            raise ValueError("Passed item is not a drone")

        self.__item = item
        self.__charge = None
        self.itemID = item.ID
        self.amount = 0
        self.amountActive = 0
        self.__dps = None
        self.projected = False
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.itemModifiedAttributes.original = self.item.attributes

    @reconstructor
    def init(self):
        self.__dps = None
        self.__item = None
        self.__charge = None

    def __fetchItemInfo(self):
        import eos.db
        self.__item = eos.db.getItem(self.itemID)
        self.__charge = None
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.item.attributes

    def __fetchChargeInfo(self):
        chargeID = self.getModifiedItemAttr("entityMissileTypeID")
        self.__chargeModifiedAttributes = ModifiedAttributeDict()
        if chargeID is not None:
            import eos.db
            charge = eos.db.getItem(int(chargeID))
            self.__charge = charge

            self.chargeModifiedAttributes.original = charge.attributes
        else:
            self.__charge = 0

    @property
    def itemModifiedAttributes(self):
        if self.__item is None:
            self.__fetchItemInfo()

        return self.__itemModifiedAttributes

    @property
    def chargeModifiedAttributes(self):
        if self.__charge is None:
            self.__fetchChargeInfo()

        return self.__chargeModifiedAttributes

    @property
    def item(self):
        if self.__item is None:
            self.__fetchItemInfo()

        return self.__item

    @property
    def charge(self):
        if self.__charge is None:
            self.__fetchChargeInfo()

        return self.__charge if self.__charge != 0 else None

    @property
    def dealsDamage(self):
        for attr in ("emDamage", "kineticDamage", "explosiveDamage", "thermalDamage"):
            if attr in self.itemModifiedAttributes or attr in self.chargeModifiedAttributes:
                return True

    @property
    def hasAmmo(self):
        return self.charge is not None

    @property
    def dps(self):
        if self.__dps == None:
            if self.dealsDamage is True and self.amountActive > 0:
                if self.hasAmmo:
                    attr = "missileLaunchDuration"
                    getter = self.getModifiedChargeAttr
                else:
                    attr =  "speed"
                    getter = self.getModifiedItemAttr

                cycleTime = self.getModifiedItemAttr(attr)
                volley = sum(map(lambda d: getter(d), self.DAMAGE_ATTRIBUTES)) * self.amountActive
                volley *= self.getModifiedItemAttr("damageMultiplier") or 1
                self.__dps = volley / (cycleTime / 1000.0)
            else:
                self.__dps = 0

        return self.__dps

    @property
    def maxRange(self):
        attrs = ("shieldTransferRange", "powerTransferRange",
                 "energyDestabilizationRange", "empFieldRange",
                 "ecmBurstRange", "maxRange")
        for attr in attrs:
            maxRange = self.getModifiedItemAttr(attr)
            if maxRange is not None: return maxRange
        if self.charge is not None:
            delay = self.getModifiedChargeAttr("explosionDelay")
            speed = self.getModifiedChargeAttr("maxVelocity")
            if delay is not None and speed is not None:
                return delay / 1000.0 * speed

    # Had to add this to match the falloff property in modules.py
    # Fscking ship scanners. If you find any other falloff attributes,
    # Put them in the attrs tuple.
    @property
    def falloff(self):
        attrs = ("falloff",)
        for attr in attrs:
            falloff = self.getModifiedItemAttr(attr)
            if falloff is not None: return falloff

    @validates("ID", "itemID", "chargeID", "amount", "amountActive")
    def validator(self, key, val):
        map = {"ID": lambda val: isinstance(val, int),
               "itemID" : lambda val: isinstance(val, int),
               "chargeID" : lambda val: isinstance(val, int),
               "amount" : lambda val: isinstance(val, int) and val >= 0,
               "amountActive" : lambda val: isinstance(val, int) and val <= self.amount and val >= 0}

        if map[key](val) == False: raise ValueError(str(val) + " is not a valid value for " + key)
        else: return val

    def clear(self):
        self.__dps = None
        self.itemModifiedAttributes.clear()
        self.chargeModifiedAttributes.clear()

    def canBeApplied(self, projectedOnto):
        """Check if drone can engage specific fitting"""
        item = self.item
        if (item.offensive and projectedOnto.ship.getModifiedItemAttr("disallowOffensiveModifiers") == 1) or \
        (item.assistive and projectedOnto.ship.getModifiedItemAttr("disallowAssistance") == 1):
            return False
        else:
            return True

    def calculateModifiedAttributes(self, fit, runTime, forceProjected = False):
        if self.projected or forceProjected:
            context = "projected", "drone"
            projected = True
        else:
            context = ("drone",)
            projected = False

        for effect in self.item.effects.itervalues():
            if effect.runTime == runTime and \
            ((projected == True and effect.isType("projected")) or \
             projected == False and effect.isType("passive")):
                i = 0
                while i != self.amountActive:
                    effect.handler(fit, self, context)
                    i += 1

        if self.charge:
            for effect in self.charge.effects.itervalues():
                if effect.runTime == runTime:
                    effect.handler(fit, self, ("droneCharge",))

    def __deepcopy__(self, memo):
        copy = Drone(self.item)
        copy.amount = self.amount
        copy.amountActive = self.amountActive
        return copy

    def fits(self, fit):
        fitDroneGroupLimits = set()
        for i in xrange(1, 3):
            groneGrp = fit.ship.getModifiedItemAttr("allowedDroneGroup%d" % i)
            if groneGrp is not None:
                fitDroneGroupLimits.add(int(groneGrp))
        if len(fitDroneGroupLimits) == 0:
            return True
        if self.item.groupID in fitDroneGroupLimits:
            return True
        return False
