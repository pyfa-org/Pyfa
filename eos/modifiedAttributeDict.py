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

from math import exp
import collections

defaultValuesCache = {}

class ItemAttrShortcut(object):
    def getModifiedItemAttr(self, key):
        if key in self.itemModifiedAttributes:
            return self.itemModifiedAttributes[key]
        else:
            return None

class ChargeAttrShortcut(object):
    def getModifiedChargeAttr(self, key):
        if key in self.chargeModifiedAttributes:
            return self.chargeModifiedAttributes[key]
        else:
            return None

class ModifiedAttributeDict(collections.MutableMapping):
    class CalculationPlaceholder():
        pass

    def __init__(self, fit = None):
        self.fit = fit
        # Stores original values of the entity
        self.__original = None
        # Modified values during calculations
        self.__intermediary = {}
        # Final modified values
        self.__modified = {}
        # Affected by entities
        self.__affectedBy = {}
        # Dictionaries for various value modification types
        self.__forced = {}
        self.__preAssigns = {}
        self.__preIncreases = {}
        self.__multipliers = {}
        self.__penalizedMultipliers = {}
        self.__postIncreases = {}

    def clear(self):
        self.__intermediary.clear()
        self.__modified.clear()
        self.__affectedBy.clear()
        self.__forced.clear()
        self.__preAssigns.clear()
        self.__preIncreases.clear()
        self.__multipliers.clear()
        self.__penalizedMultipliers.clear()
        self.__postIncreases.clear()

    @property
    def original(self):
        return self.__original

    @original.setter
    def original(self, val):
        self.__original = val
        self.__modified.clear()

    def __getitem__(self, key):
        # Check if we have final calculated value
        if key in self.__modified:
            if self.__modified[key] == self.CalculationPlaceholder:
                self.__modified[key] = self.__calculateValue(key)
            return self.__modified[key]
        # Then in values which are not yet calculated
        elif key in self.__intermediary:
            return self.__intermediary[key]
        # Original value is the least priority
        else:
            return self.getOriginal(key)

    def __delitem__(self, key):
        if key in self.__modified:
            del self.__modified[key]
        if key in self.__intermediary:
            del self.__intermediary[key]

    def getOriginal(self, key):
        val = self.__original.get(key)
        if val is None:
            return None

        return val.value if hasattr(val, "value") else val

    def __setitem__(self, key, val):
        self.__intermediary[key] = val

    def __iter__(self):
        all = dict(self.__original, **self.__modified)
        return (key for key in all)

    def __contains__(self, key):
        return (self.__original is not None and key in self.__original) or key in self.__modified or key in self.__intermediary

    def __placehold(self, key):
        """Create calculation placeholder in item's modified attribute dict"""
        self.__modified[key] = self.CalculationPlaceholder

    def __len__(self):
        keys = set()
        keys.update(self.__original.iterkeys())
        keys.update(self.__modified.iterkeys())
        keys.update(self.__intermediary.iterkeys())
        return len(keys)

    def __calculateValue(self, key):
        # If value is forced, we don't have to calculate anything,
        # just return forced value instead
        force = self.__forced[key] if key in self.__forced else None
        if force is not None:
            return force
        # Grab our values if they're there, otherwise we'll take default values
        preIncrease = self.__preIncreases[key] if key in self.__preIncreases else 0
        multiplier = self.__multipliers[key] if key in self.__multipliers else 1
        penalizedMultiplierGroups = self.__penalizedMultipliers[key] if key in self.__penalizedMultipliers else {}
        postIncrease = self.__postIncreases[key] if key in self.__postIncreases else 0

        # Grab initial value, priorities are:
        # Results of ongoing calculation > preAssign > original > 0
        try:
            default = defaultValuesCache[key]
        except KeyError:
            from eos.db.gamedata.queries import getAttributeInfo
            attrInfo = getAttributeInfo(key)
            if attrInfo is None:
                default = defaultValuesCache[key] = 0.0
            else:
                dv = attrInfo.defaultValue
                default = defaultValuesCache[key] = dv if dv is not None else 0.0
        val = self.__intermediary[key] if key in self.__intermediary else self.__preAssigns[key] if key in self.__preAssigns else self.getOriginal(key) if key in self.__original else default

        # We'll do stuff in the following order:
        # preIncrease > multiplier > stacking penalized multipliers > postIncrease
        val += preIncrease
        val *= multiplier
        # Each group is penalized independently
        # Things in different groups will not be stack penalized between each other
        for penalizedMultipliers in penalizedMultiplierGroups.itervalues():
            # A quick explanation of how this works:
            # 1: Bonuses and penalties are calculated seperately, so we'll have to filter each of them
            l1 = filter(lambda val: val > 1, penalizedMultipliers)
            l2 = filter(lambda val: val < 1, penalizedMultipliers)
            # 2: The most significant bonuses take the smallest penalty,
            # This means we'll have to sort
            abssort = lambda val: -abs(val - 1)
            l1.sort(key=abssort)
            l2.sort(key=abssort)
            # 3: The first module doesn't get penalized at all
            # Any module after the first takes penalties according to:
            # 1 + (multiplier - 1) * math.exp(- math.pow(i, 2) / 7.1289)
            for l in (l1, l2):
                for i in xrange(len(l)):
                    bonus = l[i]
                    val *= 1 + (bonus - 1) * exp(- i ** 2 / 7.1289)
        val += postIncrease

        return val

    def getAfflictions(self, key):
        return self.__affectedBy[key] if key in self.__affectedBy else {}

    def iterAfflictions(self):
        return self.__affectedBy.__iter__()

    def __afflict(self, attributeName, operation, bonus):
        """Add modifier to list of things affecting current item"""
        # Do nothing if no fit is assigned
        if self.fit is None:
            return
        # Create dictionary for given attribute and give it alias
        if attributeName not in self.__affectedBy:
            self.__affectedBy[attributeName] = {}
        affs = self.__affectedBy[attributeName]
        # If there's no set for current fit in dictionary, create it
        if self.fit not in affs:
            affs[self.fit] = set()
        # Reassign alias to set
        affs = affs[self.fit]
        # Get modifier which helps to compose 'Affected by' map
        modifier = self.fit.getModifier()
        # Add current affliction to set
        affs.add((modifier, operation, bonus))

    def preAssign(self, attributeName, value):
        """Overwrites original value of the entity with given one, allowing further modification"""
        self.__preAssigns[attributeName] = value
        self.__placehold(attributeName)
        # Add to afflictions only if preassigned value differs from original
        if value != self.getOriginal(attributeName):
            self.__afflict(attributeName, "=", value)

    def increase(self, attributeName, increase, position="pre"):
        """Increase value of given attribute by given number"""
        # Increases applied before multiplications and after them are
        # written in separate maps
        if position == "pre":
            tbl = self.__preIncreases
        elif position == "post":
            tbl = self.__postIncreases
        else:
            raise ValueError("position should be either pre or post")
        if not attributeName in tbl:
            tbl[attributeName] = 0
        tbl[attributeName] += increase
        self.__placehold(attributeName)
        # Add to list of afflictions only if we actually modify value
        if increase != 0:
            self.__afflict(attributeName, "+", increase)

    def multiply(self, attributeName, multiplier, stackingPenalties=False, penaltyGroup="default"):
        """Multiply value of given attribute by given factor"""
        # If we're asked to do stacking penalized multiplication, append values
        # to per penalty group lists
        if stackingPenalties:
            if not attributeName in self.__penalizedMultipliers:
                self.__penalizedMultipliers[attributeName] = {}
            if not penaltyGroup in self.__penalizedMultipliers[attributeName]:
                self.__penalizedMultipliers[attributeName][penaltyGroup] = []
            tbl = self.__penalizedMultipliers[attributeName][penaltyGroup]
            tbl.append(multiplier)
        # Non-penalized multiplication factors go to the single list
        else:
            if not attributeName in self.__multipliers:
                self.__multipliers[attributeName] = 1
            self.__multipliers[attributeName] *= multiplier
        self.__placehold(attributeName)
        # Add to list of afflictions only if we actually modify value
        if multiplier != 1:
            self.__afflict(attributeName, "%s*" % ("s" if stackingPenalties else ""), multiplier)

    def boost(self, attributeName, boostFactor, *args, **kwargs):
        """Boost value by some percentage"""
        # We just transform percentage boost into multiplication factor
        self.multiply(attributeName, 1 + boostFactor / 100.0, *args, **kwargs)

    def force(self, attributeName, value):
        """Force value to attribute and prohibit any changes to it"""
        self.__forced[attributeName] = value
        self.__placehold(attributeName)
        self.__afflict(attributeName, u"\u2263", value)

class Affliction():
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount
