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

# Cargo class copied from Implant class and hacked to make work. \o/
# @todo: clean me up, Scotty
class Cargo(HandledItem, HandledCharge, ItemAttrShortcut, ChargeAttrShortcut):

    def __init__(self, item):
        if item.category.name != "Charge":
            raise ValueError("Passed item is not a charge")

        self.__item = item
        self.itemID = item.ID
        self.active = True
        self.amount = 0
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.item.attributes

    @reconstructor
    def init(self):
        self.__item = None

    def __fetchItemInfo(self):
        import eos.db
        self.__item = eos.db.getItem(self.itemID)
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.__item.attributes

    @property
    def itemModifiedAttributes(self):
        if self.__item is None:
            self.__fetchItemInfo()

        return self.__itemModifiedAttributes

    @property
    def item(self):
        if self.__item is None:
            self.__fetchItemInfo()

        return self.__item

    def clear(self):
        self.itemModifiedAttributes.clear()

    @validates("fitID", "itemID", "active")
    def validator(self, key, val):
        map = {"fitID": lambda val: isinstance(val, int),
               "itemID" : lambda val: isinstance(val, int),
               "active": lambda val: isinstance(val, bool)}

        if map[key](val) == False: raise ValueError(str(val) + " is not a valid value for " + key)
        else: return val

    def __deepcopy__(self, memo):
        copy = Cargo(self.item)
        copy.active = self.active
        return copy