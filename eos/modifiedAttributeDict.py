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


from collections.abc import MutableMapping
from copy import copy
from math import exp

from eos.const import Operator
# TODO: This needs to be moved out, we shouldn't have *ANY* dependencies back to other modules/methods inside eos.
# This also breaks writing any tests. :(
from eos.db.gamedata.queries import getAttributeInfo


defaultValuesCache = {}
cappingAttrKeyCache = {}
resistanceCache = {}


def getAttrDefault(key, fallback=None):
    try:
        default = defaultValuesCache[key]
    except KeyError:
        attrInfo = getAttributeInfo(key)
        if attrInfo is None:
            default = defaultValuesCache[key] = None
        else:
            default = defaultValuesCache[key] = attrInfo.defaultValue
    if default is None:
        default = fallback
    return default


def getResistanceAttrID(modifyingItem, effect):
    # If it doesn't exist on the effect, check the modifying module's attributes.
    # If it's there, cache it and return
    if effect.resistanceID:
        return effect.resistanceID
    cacheKey = (modifyingItem.item.ID, effect.ID)
    try:
        return resistanceCache[cacheKey]
    except KeyError:
        attrPrefix = effect.getattr('prefix')
        if attrPrefix:
            resistanceID = int(modifyingItem.getModifiedItemAttr('{}ResistanceID'.format(attrPrefix))) or None
            if not resistanceID:
                resistanceID = int(modifyingItem.getModifiedItemAttr('{}RemoteResistanceID'.format(attrPrefix))) or None
        else:
            resistanceID = int(modifyingItem.getModifiedItemAttr("remoteResistanceID")) or None
        resistanceCache[cacheKey] = resistanceID
        return resistanceID


class ItemAttrShortcut:

    def getModifiedItemAttr(self, key, default=0):
        return_value = self.itemModifiedAttributes.get(key)
        return return_value if return_value is not None else default

    def getModifiedItemAttrExtended(self, key, extraMultipliers=None, ignoreAfflictors=(), default=0):
        return_value = self.itemModifiedAttributes.getExtended(key, extraMultipliers=extraMultipliers, ignoreAfflictors=ignoreAfflictors)
        return return_value if return_value is not None else default

    def getItemBaseAttrValue(self, key, default=0):
        return_value = self.itemModifiedAttributes.getOriginal(key)
        return return_value if return_value is not None else default


class ChargeAttrShortcut:

    def getModifiedChargeAttr(self, key, default=0):
        return_value = self.chargeModifiedAttributes.get(key)
        return return_value if return_value is not None else default

    def getModifiedChargeAttrExtended(self, key, extraMultipliers=None, ignoreAfflictors=(), default=0):
        return_value = self.chargeModifiedAttributes.getExtended(key, extraMultipliers=extraMultipliers, ignoreAfflictors=ignoreAfflictors)
        return return_value if return_value is not None else default

    def getChargeBaseAttrValue(self, key, default=0):
        return_value = self.chargeModifiedAttributes.getOriginal(key)
        return return_value if return_value is not None else default


class ModifiedAttributeDict(MutableMapping):
    overrides_enabled = False

    class CalculationPlaceholder:
        def __init__(self):
            pass

    def __init__(self, fit=None, parent=None):
        self.__fit = fit
        self.parent = parent
        # Stores original values of the entity
        self.__original = None
        # Modified values during calculations
        self.__intermediary = {}
        # Final modified values
        self.__modified = {}
        # Affected by entities
        # Format:
        # {attr name: {modifying fit: (
        #   modifying item, operation, stacking group, pre-resist amount,
        #   post-resist amount, affects result or not)}}
        self.__affectedBy = {}
        # Overrides (per item)
        self.__overrides = {}
        # Mutators (per module)
        self.__mutators = {}
        # Dictionaries for various value modification types
        self.__forced = {}
        self.__preAssigns = {}
        self.__preIncreases = {}
        self.__multipliers = {}
        self.__penalizedMultipliers = {}
        self.__postIncreases = {}
        # We sometimes override the modifier (for things like skill handling). Store it here instead of registering it
        # with the fit (which could cause bug for items that have both item bonuses and skill bonus, ie Subsystems)
        self.__tmpModifier = None

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
    def fit(self):
        # self.fit is usually set during fit calculations when the item is registered with the fit. However,
        # under certain circumstances, an effect will not work as it will try to modify an item which has NOT
        # yet been registered and thus has not had self.fit set. In this case, use the modules owner attribute
        # to point to the correct fit. See GH Issue #434
        if self.__fit is not None:
            return self.__fit
        if hasattr(self.parent, 'owner'):
            return self.parent.owner
        return None

    @fit.setter
    def fit(self, fit):
        self.__fit = fit

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

    @property
    def mutators(self):
        return {x.attribute.name: x for x in self.__mutators.values()}

    @mutators.setter
    def mutators(self, val):
        self.__mutators = val

    def __getitem__(self, key):
        # Check if we have final calculated value
        val = self.__modified.get(key)
        if val is self.CalculationPlaceholder:
            val = self.__modified[key] = self.__calculateValue(key)
        if val is not None:
            return val

        # Then in values which are not yet calculated
        if self.__intermediary:
            val = self.__intermediary.get(key)
        else:
            val = None
        if val is not None:
            return val

        # Original value is the least priority
        return self.getOriginal(key)

    def getExtended(self, key, extraMultipliers=None, ignoreAfflictors=None, default=0):
        """
        Here we consider couple of parameters. If they affect final result, we do
        not store result, and if they are - we do.
        """
        # Here we do not have support for preAssigns/forceds, as doing them would
        # mean that we have to store all of them in a list which increases memory use,
        # and we do not actually need those operators atm
        preIncreaseAdjustment = 0
        multiplierAdjustment = 1
        ignorePenalizedMultipliers = {}
        postIncreaseAdjustment = 0
        for fit, afflictors in self.getAfflictions(key).items():
            for afflictor, operator, stackingGroup, preResAmount, postResAmount, used in afflictors:
                if afflictor in ignoreAfflictors:
                    if operator == Operator.MULTIPLY:
                        if stackingGroup is None:
                            multiplierAdjustment /= postResAmount
                        else:
                            ignorePenalizedMultipliers.setdefault(stackingGroup, []).append(postResAmount)
                    elif operator == Operator.PREINCREASE:
                        preIncreaseAdjustment -= postResAmount
                    elif operator == Operator.POSTINCREASE:
                        postIncreaseAdjustment -= postResAmount

        # If we apply no customizations - use regular getter
        if (
            not extraMultipliers and
            preIncreaseAdjustment == 0 and multiplierAdjustment == 1 and
            postIncreaseAdjustment == 0 and len(ignorePenalizedMultipliers) == 0
        ):
            return self.get(key, default=default)

        # Try to calculate custom values
        val = self.__calculateValue(
            key, extraMultipliers=extraMultipliers, preIncAdj=preIncreaseAdjustment, multAdj=multiplierAdjustment,
            postIncAdj=postIncreaseAdjustment, ignorePenMult=ignorePenalizedMultipliers)
        if val is not None:
            return val

        # Then the same fallbacks as in regular getter
        if self.__intermediary:
            val = self.__intermediary.get(key)
        else:
            val = None
        if val is not None:
            return val
        val = self.getOriginal(key)
        if val is not None:
            return val
        return default

    def __delitem__(self, key):
        if key in self.__modified:
            del self.__modified[key]
        if key in self.__intermediary:
            del self.__intermediary[key]

    def getOriginal(self, key, default=None):
        val = None
        if self.overrides_enabled and self.overrides:
            val = self.overrides.get(key, val)

        # mutators are overriden by overrides. x_x
        val = self.mutators.get(key, val)

        if val is None:
            if self.original:
                val = self.original.get(key, val)

        if val is None:
            val = getAttrDefault(key, fallback=None)

        if val is None and val != default:
            val = default

        return val.value if hasattr(val, "value") else val

    def __setitem__(self, key, val):
        self.__intermediary[key] = val

    def __iter__(self):
        all_dict = dict(self.original, **self.__modified)
        return (key for key in all_dict)

    def __contains__(self, key):
        return (self.original is not None and key in self.original) or \
               key in self.__modified or key in self.__intermediary

    def __placehold(self, key):
        """Create calculation placeholder in item's modified attribute dict"""
        self.__modified[key] = self.CalculationPlaceholder

    def __len__(self):
        keys = set()
        keys.update(iter(self.original.keys()))
        keys.update(iter(self.__modified.keys()))
        keys.update(iter(self.__intermediary.keys()))
        return len(keys)

    def __calculateValue(self, key, extraMultipliers=None, preIncAdj=None, multAdj=None, postIncAdj=None, ignorePenMult=None):
        # It's possible that various attributes are capped by other attributes,
        # it's defined by reference maxAttributeID
        try:
            cappingKey = cappingAttrKeyCache[key]
        except KeyError:
            attrInfo = getAttributeInfo(key)
            if attrInfo is None:
                cappingId = cappingAttrKeyCache[key] = None
            else:
                cappingId = attrInfo.maxAttributeID
            if cappingId is None:
                cappingKey = None
            else:
                cappingAttrInfo = getAttributeInfo(cappingId)
                cappingKey = None if cappingAttrInfo is None else cappingAttrInfo.name
                cappingAttrKeyCache[key] = cappingKey

        if cappingKey:
            cappingValue = self.original.get(cappingKey, self.__calculateValue(cappingKey))
            cappingValue = cappingValue.value if hasattr(cappingValue, "value") else cappingValue
        else:
            cappingValue = None

        # If value is forced, we don't have to calculate anything,
        # just return forced value instead
        force = self.__forced[key] if key in self.__forced else None
        if force is not None:
            if cappingValue is not None:
                force = min(force, cappingValue)
            if key in ("cpu", "power", "cpuOutput", "powerOutput"):
                force = round(force, 2)
            return force
        # Grab our values if they're there, otherwise we'll take default values
        preIncrease = self.__preIncreases.get(key, 0)
        multiplier = self.__multipliers.get(key, 1)
        penalizedMultiplierGroups = self.__penalizedMultipliers.get(key, {})
        # Add extra multipliers to the group, not modifying initial data source
        if extraMultipliers is not None:
            penalizedMultiplierGroups = copy(penalizedMultiplierGroups)
            for stackGroup, operationsData in extraMultipliers.items():
                multipliers = []
                for mult, resAttrID in operationsData:
                    if not resAttrID:
                        multipliers.append(mult)
                        continue
                    resAttrInfo = getAttributeInfo(resAttrID)
                    if not resAttrInfo:
                        multipliers.append(mult)
                        continue
                    resMult = self.fit.ship.itemModifiedAttributes[resAttrInfo.attributeName]
                    if resMult is None or resMult == 1:
                        multipliers.append(mult)
                        continue
                    mult = (mult - 1) * resMult + 1
                    multipliers.append(mult)
                penalizedMultiplierGroups[stackGroup] = penalizedMultiplierGroups.get(stackGroup, []) + multipliers
        postIncrease = self.__postIncreases.get(key, 0)

        # Grab initial value, priorities are:
        # Results of ongoing calculation > preAssign > original > 0
        default = getAttrDefault(key, fallback=0.0)
        val = self.__intermediary.get(key, self.__preAssigns.get(key, self.getOriginal(key, default)))

        # We'll do stuff in the following order:
        # preIncrease > multiplier > stacking penalized multipliers > postIncrease
        val += preIncrease
        if preIncAdj is not None:
            val += preIncAdj
        val *= multiplier
        if multAdj is not None:
            val *= multAdj
        # Each group is penalized independently
        # Things in different groups will not be stack penalized between each other
        for penaltyGroup, penalizedMultipliers in penalizedMultiplierGroups.items():
            if ignorePenMult is not None and penaltyGroup in ignorePenMult:
                # Avoid modifying source and remove multipliers we were asked to remove for this calc
                penalizedMultipliers = penalizedMultipliers[:]
                for ignoreMult in ignorePenMult[penaltyGroup]:
                    try:
                        penalizedMultipliers.remove(ignoreMult)
                    except ValueError:
                        pass
            # A quick explanation of how this works:
            # 1: Bonuses and penalties are calculated seperately, so we'll have to filter each of them
            l1 = [_val for _val in penalizedMultipliers if _val > 1]
            l2 = [_val for _val in penalizedMultipliers if _val < 1]
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
                    val *= 1 + (bonus - 1) * exp(- i ** 2 / 7.1289)
        val += postIncrease
        if postIncAdj is not None:
            val += postIncAdj

        # Cap value if we have cap defined
        if cappingValue is not None:
            val = min(val, cappingValue)
        if key in ("cpu", "power", "cpuOutput", "powerOutput"):
            val = round(val, 2)
        return val

    def __handleSkill(self, skillName):
        """
        Since ship skill bonuses do not directly modify the attributes, it does
        not register as an affector (instead, the ship itself is the affector).
        To fix this, we pass the skill which ends up here, where we register it
        with the fit and thus get the correct affector. Returns skill level to
        be used to modify modifier. See GH issue #101
        """
        skill = self.fit.character.getSkill(skillName)
        self.__tmpModifier = skill
        return skill.level

    def getAfflictions(self, key):
        return self.__affectedBy.get(key, {})

    def iterAfflictions(self):
        return self.__affectedBy.__iter__()

    def __afflict(self, attributeName, operator, stackingGroup, preResAmount, postResAmount, used=True):
        """Add modifier to list of things affecting current item"""
        # Do nothing if no fit is assigned
        fit = self.fit
        if fit is None:
            return
        # Create dictionary for given attribute and give it alias
        if attributeName not in self.__affectedBy:
            self.__affectedBy[attributeName] = {}
        affs = self.__affectedBy[attributeName]
        origin = fit.getOrigin()
        fit = origin if origin and origin != fit else fit
        # If there's no set for current fit in dictionary, create it
        if fit not in affs:
            affs[fit] = []
        # Reassign alias to list
        affs = affs[fit]
        # Get modifier which helps to compose 'Affected by' map

        if self.__tmpModifier:
            modifier = self.__tmpModifier
            self.__tmpModifier = None
        else:
            modifier = fit.getModifier()

        # Add current affliction to list
        affs.append((modifier, operator, stackingGroup, preResAmount, postResAmount, used))

    def preAssign(self, attributeName, value, **kwargs):
        """Overwrites original value of the entity with given one, allowing further modification"""
        self.__preAssigns[attributeName] = value
        self.__placehold(attributeName)
        self.__afflict(attributeName, Operator.PREASSIGN, None, value, value, value != self.getOriginal(attributeName))

    def increase(self, attributeName, increase, position="pre", skill=None, **kwargs):
        """Increase value of given attribute by given number"""
        if skill:
            increase *= self.__handleSkill(skill)

        if 'effect' in kwargs:
            increase *= ModifiedAttributeDict.getResistance(self.fit, kwargs['effect']) or 1

        # Increases applied before multiplications and after them are
        # written in separate maps
        if position == "pre":
            operator = Operator.PREINCREASE
            tbl = self.__preIncreases
        elif position == "post":
            operator = Operator.POSTINCREASE
            tbl = self.__postIncreases
        else:
            raise ValueError("position should be either pre or post")
        if attributeName not in tbl:
            tbl[attributeName] = 0
        tbl[attributeName] += increase
        self.__placehold(attributeName)
        self.__afflict(attributeName, operator, None, increase, increase, increase != 0)

    def multiply(self, attributeName, multiplier, stackingPenalties=False, penaltyGroup="default", skill=None, **kwargs):
        """Multiply value of given attribute by given factor"""
        if multiplier is None:  # See GH issue 397
            return

        if skill:
            multiplier *= self.__handleSkill(skill)

        preResMultiplier = multiplier
        resisted = False
        # Goddammit CCP, make up your mind where you want this information >.< See #1139
        if 'effect' in kwargs:
            resistFactor = ModifiedAttributeDict.getResistance(self.fit, kwargs['effect']) or 1
            if resistFactor != 1:
                resisted = True
                multiplier = (multiplier - 1) * resistFactor + 1

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

        afflictPenal = ""
        if stackingPenalties:
            afflictPenal += "s"
        if resisted:
            afflictPenal += "r"

        self.__afflict(
            attributeName, Operator.MULTIPLY, penaltyGroup if stackingPenalties else None,
            preResMultiplier, multiplier, multiplier != 1)

    def boost(self, attributeName, boostFactor, skill=None, **kwargs):
        """Boost value by some percentage"""
        if skill:
            boostFactor *= self.__handleSkill(skill)

        # We just transform percentage boost into multiplication factor
        self.multiply(attributeName, 1 + boostFactor / 100.0, **kwargs)

    def force(self, attributeName, value, **kwargs):
        """Force value to attribute and prohibit any changes to it"""
        self.__forced[attributeName] = value
        self.__placehold(attributeName)
        self.__afflict(attributeName, Operator.FORCE, None, value, value)

    @staticmethod
    def getResistance(fit, effect):
        # Resistances are applicable only to projected effects
        if isinstance(effect.type, (tuple, list)):
            effectType = effect.type
        else:
            effectType = (effect.type,)
        if 'projected' not in effectType:
            return 1
        remoteResistID = getResistanceAttrID(modifyingItem=fit.getModifier(), effect=effect)
        if not remoteResistID:
            return 1
        attrInfo = getAttributeInfo(remoteResistID)
        # Get the attribute of the resist
        resist = fit.ship.itemModifiedAttributes[attrInfo.attributeName] or None
        return resist or 1


class Affliction:
    def __init__(self, affliction_type, amount):
        self.type = affliction_type
        self.amount = amount
