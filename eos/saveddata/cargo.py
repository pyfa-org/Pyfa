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

import sys
from logbook import Logger

from sqlalchemy.orm import validates, reconstructor

import eos.db
from eos.effectHandlerHelpers import HandledItem
from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut

pyfalog = Logger(__name__)


class Cargo(HandledItem, ItemAttrShortcut):
    def __init__(self, item):
        """Initialize cargo from the program"""
        self.__item = item
        self.itemID = item.ID if item is not None else None
        self.amount = 0
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = item.attributes
        self.__itemModifiedAttributes.overrides = item.overrides

    @reconstructor
    def init(self):
        """Initialize cargo from the database and validate"""
        self.__item = None

        if self.itemID:
            self.__item = eos.db.getItem(self.itemID)
            if self.__item is None:
                pyfalog.error("Item (id: {0}) does not exist", self.itemID)
                return

        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.__item.attributes
        self.__itemModifiedAttributes.overrides = self.__item.overrides

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    @property
    def isInvalid(self):
        return self.__item is None

    @property
    def item(self):
        return self.__item

    def clear(self):
        self.itemModifiedAttributes.clear()

    @validates("fitID", "itemID", "amount")
    def validator(self, key, val):
        map = {
            "fitID" : lambda _val: isinstance(_val, int),
            "itemID": lambda _val: isinstance(_val, int),
            "amount": lambda _val: isinstance(_val, int)
        }

        if key == "amount" and val > sys.maxint:
            val = sys.maxint

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def __deepcopy__(self, memo):
        copy = Cargo(self.item)
        copy.amount = self.amount
        return copy
