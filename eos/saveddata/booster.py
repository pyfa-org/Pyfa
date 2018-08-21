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

from logbook import Logger

from sqlalchemy.orm import reconstructor, validates

import eos.db
from eos.effectHandlerHelpers import HandledItem
from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut
from eos.saveddata.boosterSideEffect import BoosterSideEffect

pyfalog = Logger(__name__)


class Booster(HandledItem, ItemAttrShortcut):
    def __init__(self, item):
        self.__item = item

        if self.isInvalid:
            raise ValueError("Passed item is not a Booster")

        self.itemID = item.ID if item is not None else None
        self.active = True

        self.__sideEffects = self.__getSideEffects()

        self.build()

    @reconstructor
    def init(self):
        """Initialize a booster from the database and validate"""
        self.__item = None

        if self.itemID:
            self.__item = eos.db.getItem(self.itemID)
            if self.__item is None:
                pyfalog.error("Item (id: {0}) does not exist", self.itemID)
                return

        if self.isInvalid:
            pyfalog.error("Item (id: {0}) is not a Booster", self.itemID)
            return

        self.build()

    def build(self):
        """ Build object. Assumes proper and valid item already set """
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.__item.attributes
        self.__itemModifiedAttributes.overrides = self.__item.overrides
        self.__slot = self.__calculateSlot(self.__item)

        if len(self.sideEffects) != len(self.__getSideEffects()):
            self.__sideEffects = []
            for ability in self.__getSideEffects():
                self.__sideEffects.append(ability)

    @property
    def sideEffects(self):
        return self.__sideEffects or []

    @property
    def activeSideEffectEffects(self):
        return [x.effect for x in self.sideEffects if x.active]

    def __getSideEffects(self):
        """Returns list of BoosterSideEffect that are loaded with data"""
        return [BoosterSideEffect(effect) for effect in self.item.effects.values() if effect.isType("boosterSideEffect")]

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    @property
    def isInvalid(self):
        return self.__item is None or self.__item.group.name != "Booster"

    @property
    def slot(self):
        return self.__slot

    @property
    def item(self):
        return self.__item

    @staticmethod
    def __calculateSlot(item):
        if "boosterness" not in item.attributes:
            raise ValueError("Passed item is not a booster")

        return int(item.attributes["boosterness"].value)

    def clear(self):
        self.itemModifiedAttributes.clear()

    def calculateModifiedAttributes(self, fit, runTime, forceProjected=False):
        if forceProjected:
            return
        if not self.active:
            return

        for effect in self.item.effects.values():
            if effect.runTime == runTime and \
                    (effect.isType("passive") or effect.isType("boosterSideEffect")):
                if effect.isType("boosterSideEffect") and effect not in self.activeSideEffectEffects:
                    continue
                effect.handler(fit, self, ("booster",))

    @validates("ID", "itemID", "ammoID", "active")
    def validator(self, key, val):
        map = {
            "ID"    : lambda _val: isinstance(_val, int),
            "itemID": lambda _val: isinstance(_val, int),
            "ammoID": lambda _val: isinstance(_val, int),
            "active": lambda _val: isinstance(_val, bool),
            "slot"  : lambda _val: isinstance(_val, int) and 1 <= _val <= 3
        }

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def __deepcopy__(self, memo):
        copy = Booster(self.item)
        copy.active = self.active

        for sideEffect in self.sideEffects:
            copyEffect = next(filter(lambda eff: eff.effectID == sideEffect.effectID, copy.sideEffects))
            copyEffect.active = sideEffect.active

        return copy
