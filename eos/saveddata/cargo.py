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
import eos.db


class Cargo(HandledItem, ItemAttrShortcut):

    def __init__(self, item):
        """Initialize cargo from the program"""
        self.__item = item
        self.__invalid = False
        self.itemID = item.ID if item is not None else None
        self.amount = 0
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = item.attributes

    @reconstructor
    def init(self):
        """Initialize cargo from the database and validate"""
        self.__item = None
        self.__invalid = False
        self.__itemModifiedAttributes = ModifiedAttributeDict()

        if self.itemID:
            # if item does not exist, set invalid
            item = eos.db.getItem(self.itemID)
            if item is None:
                self.__invalid = True
            self.__item = item

        if self.__item:
            self.__itemModifiedAttributes.original = self.__item.attributes

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    @property
    def isInvalid(self):
        return self.__invalid

    @property
    def item(self):
        return self.__item

    def clear(self):
        self.itemModifiedAttributes.clear()

    @validates("fitID", "itemID")
    def validator(self, key, val):
        map = {"fitID": lambda val: isinstance(val, int),
               "itemID" : lambda val: isinstance(val, int)}

        if map[key](val) == False: raise ValueError(str(val) + " is not a valid value for " + key)
        else: return val

    def __deepcopy__(self, memo):
        copy = Cargo(self.item)
        copy.amount = self.amount
        return copy
