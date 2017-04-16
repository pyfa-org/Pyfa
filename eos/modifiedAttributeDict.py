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

import collections
from math import exp

defaultValuesCache = {}
cappingAttrKeyCache = {}


class ItemAttrShortcut(object):
    def getModifiedItemAttr(self, key, default=None):
        if key in self.itemModifiedAttributes:
            return self.itemModifiedAttributes[key]
        else:
            return default


class ChargeAttrShortcut(object):
    def getModifiedChargeAttr(self, key, default=None):
        if key in self.chargeModifiedAttributes:
            return self.chargeModifiedAttributes[key]
        else:
            return default


class ModifiedAttributeDict(collections.MutableMapping):
    OVERRIDES = False

    class CalculationPlaceholder(object):
        def __init__(self):
            pass

    def __init__(self, fit=None, parent=None):
        self.parent = parent
        self.fit = fit
        # Stores original values of the entity
        self.__original = None
        # Modified values during calculations
        self.__intermediary = {}
        # Final modified values
        self.__modified = {}
        # Affected by entities
        self.__affectedBy = {}
        # Overrides
        self.__overrides = {}
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

    @property
    def overrides(self):
        return self.__overrides

    @overrides.setter
    def overrides(self, val):
        self.__overrides = val

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
        if self.OVERRIDES and key in self.__overrides:
            return self.__overrides.get(key).value
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
        return (self.__original is not None and key in self.__original) or \
            key in self.__modified or key in self.__intermediary

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
        # It's possible that various attributes are capped by other attributes,
        # it's defined by reference maxAttributeID
        try:
            cappingKey = cappingAttrKeyCache[key]
        except KeyError:
            from eos.db.gamedata.queries import getAttributeInfo
            attrInfo = getAttributeInfo(key)
            if attrInfo is None:
                cappingId = cappingAttrKeyCache[key] = None
            else:
                # see GH issue #620
                cappingId = cappingAttrKeyCache[key] = attrInfo.maxAttributeID
            if cappingId is None:
                cappingKey = None
            else:
                cappingAttrInfo = getAttributeInfo(cappingId)
                cappingKey = None if cappingAttrInfo is None else cappingAttrInfo.name

        if cappingKey:
            if cappingKey in self.original:
                #  some items come with their own caps (ie: carriers). If they do, use this
                cappingValue = self.original.get(cappingKey).value
            else:
                # If not, get info about the default value
                cappingValue = self.__calculateValue(cappingKey)
        else:
            cappingValue = None

        # If value is forced, we don't have to calculate anything,
        # just return forced value instead
        force = self.__forced[key] if key in self.__forced else None
        if force is not None:
            if cappingValue is not None:
                force = min(force, cappingValue)
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
        val = self.__intermediary[key] if key in self.__intermediary else self.__preAssigns[
            key] if key in self.__preAssigns else self.getOriginal(key) if key in self.__original else default

        # We'll do stuff in the following order:
        # preIncrease > multiplier > stacking penalized multipliers > postIncrease
        val += preIncrease
        val *= multiplier
        # Each group is penalized independently
        # Things in different groups will not be stack penalized between each other
        for penalizedMultipliers in penalizedMultiplierGroups.itervalues():
            # A quick explanation of how this works:
            # 1: Bonuses and penalties are calculated seperately, so we'll have to filter each of them
            l1 = filter(lambda _val: _val > 1, penalizedMultipliers)
            l2 = filter(lambda _val: _val < 1, penalizedMultipliers)
            # 2: The most significant bonuses take the smallest penalty,
            # This means we'll have to sort
            abssort = lambda _val: -abs(_val - 1)
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

        # Cap value if we have cap defined
        if cappingValue is not None:
            val = min(val, cappingValue)

        return val

    def __handleSkill(self, skillName):
        """
        Since ship skill bonuses do not directly modify the attributes, it does
        not register as an affector (instead, the ship itself is the affector).
        To fix this, we pass the skill which ends up here, where we register it
        with the fit and thus get the correct affector. Returns skill level to
        be used to modify modifier. See GH issue #101
        """
        fit = self.fit
        if not fit:
            # self.fit is usually set during fit calculations when the item is registered with the fit. However,
            # under certain circumstances, an effect will not work as it will try to modify an item which has NOT
            # yet been registered and thus has not had self.fit set. In this case, use the modules owner attribute
            # to point to the correct fit. See GH Issue #434
            fit = self.parent.owner
        skill = fit.character.getSkill(skillName)
        fit.register(skill)
        return skill.level

    def getAfflictions(self, key):
        return self.__affectedBy[key] if key in self.__affectedBy else {}

    def iterAfflictions(self):
        return self.__affectedBy.__iter__()

    def __afflict(self, attributeName, operation, bonus, used=True):
        """Add modifier to list of things affecting current item"""
        # Do nothing if no fit is assigned
        if self.fit is None:
            return
        # Create dictionary for given attribute and give it alias
        if attributeName not in self.__affectedBy:
            self.__affectedBy[attributeName] = {}
        affs = self.__affectedBy[attributeName]
        origin = self.fit.getOrigin()
        fit = origin if origin and origin != self.fit else self.fit
        # If there's no set for current fit in dictionary, create it
        if fit not in affs:
            affs[fit] = []
        # Reassign alias to list
        affs = affs[fit]
        # Get modifier which helps to compose 'Affected by' map
        modifier = self.fit.getModifier()

        # Add current affliction to list
        affs.append((modifier, operation, bonus, used))

    def preAssign(self, attributeName, value):
        """Overwrites original value of the entity with given one, allowing further modification"""
        self.__preAssigns[attributeName] = value
        self.__placehold(attributeName)
        self.__afflict(attributeName, "=", value, value != self.getOriginal(attributeName))

    def increase(self, attributeName, increase, position="pre", skill=None):
        """Increase value of given attribute by given number"""
        if skill:
            increase *= self.__handleSkill(skill)

        # Increases applied before multiplications and after them are
        # written in separate maps
        if position == "pre":
            tbl = self.__preIncreases
        elif position == "post":
            tbl = self.__postIncreases
        else:
            raise ValueError("position should be either pre or post")
        if attributeName not in tbl:
            tbl[attributeName] = 0
        tbl[attributeName] += increase
        self.__placehold(attributeName)
        self.__afflict(attributeName, "+", increase, increase != 0)

    def multiply(self, attributeName, multiplier, stackingPenalties=False, penaltyGroup="default", skill=None):
        """Multiply value of given attribute by given factor"""
        if multiplier is None:  # See GH issue 397
            return

        if skill:
            multiplier *= self.__handleSkill(skill)

        # If we're asked to do stacking penalized multiplication, append values
        # to per penalty group lists
        if stackingPenalties:
            if attributeName not in self.__penalizedMultipliers:
                self.__penalizedMultipliers[attributeName] = {}
            if penaltyGroup not in self.__penalizedMultipliers[attributeName]:
                self.__penalizedMultipliers[attributeName][penaltyGroup] = []
            tbl = self.__penalizedMultipliers[attributeName][penaltyGroup]
            tbl.append(multiplier)
        # Non-penalized multiplication factors go to the single list
        else:
            if attributeName not in self.__multipliers:
                self.__multipliers[attributeName] = 1
            self.__multipliers[attributeName] *= multiplier

        self.__placehold(attributeName)
        self.__afflict(attributeName, "%s*" % ("s" if stackingPenalties else ""), multiplier, multiplier != 1)

    def boost(self, attributeName, boostFactor, skill=None, remoteResists=False, *args, **kwargs):
        """Boost value by some percentage"""
        if skill:
            boostFactor *= self.__handleSkill(skill)

        if remoteResists:
            # @todo: this is such a disgusting hack. Look into sending these checks to the module class before the
            # effect is applied.
            mod = self.fit.getModifier()
            remoteResistID = mod.getModifiedItemAttr("remoteResistanceID") or None

            # We really don't have a way of getting a ships attribute by ID. Fail.
            resist = next((x for x in self.fit.ship.item.attributes.values() if x.ID == remoteResistID), None)

            if remoteResistID and resist:
                boostFactor *= resist.value

        # We just transform percentage boost into multiplication factor
        self.multiply(attributeName, 1 + boostFactor / 100.0, *args, **kwargs)

    def force(self, attributeName, value):
        """Force value to attribute and prohibit any changes to it"""
        self.__forced[attributeName] = value
        self.__placehold(attributeName)
        self.__afflict(attributeName, u"\u2263", value)


class Affliction(object):
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount
