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

from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut
from eos.effectHandlerHelpers import HandledItem

class Ship(ItemAttrShortcut, HandledItem):
    def __init__(self, item):
        self.__item = item
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        if not isinstance(item, int):
            self.__buildOriginal()

        self.commandBonus = 0

    def __fetchItemInfo(self):
        import eos.db
        self.__item = eos.db.getItem(self.__item)
        self.__buildOriginal()

    def __buildOriginal(self):
        self.__itemModifiedAttributes.original = self.item.attributes

    @property
    def item(self):
        if isinstance(self.__item, int):
            self.__fetchItemInfo()

        return self.__item

    @property
    def itemModifiedAttributes(self):
        if isinstance(self.__item, int):
            self.__fetchItemInfo()

        return self.__itemModifiedAttributes

    def clear(self):
        self.itemModifiedAttributes.clear()
        self.commandBonus = 0

    def calculateModifiedAttributes(self, fit, runTime, forceProjected = False):
        if forceProjected: return
        for effect in self.item.effects.itervalues():
            if effect.runTime == runTime and effect.isType("passive"):
                effect.handler(fit, self, ("ship",))

    def __deepcopy__(self, memo):
        copy = Ship(self.item)
        return copy
