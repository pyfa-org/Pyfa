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
from eos.saveddata.mode import Mode
import eos.db

class Ship(ItemAttrShortcut, HandledItem):
    def __init__(self, item):

        if item.category.name != "Ship":
            raise ValueError('Passed item "%s" (category: (%s)) is not under Ship category'%(item.name, item.category.name))

        self.__item = item
        self.__modeItems = self.__getModeItems()
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.item.attributes

        self.commandBonus = 0

    @property
    def item(self):
        return self.__item

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    def clear(self):
        self.itemModifiedAttributes.clear()
        self.commandBonus = 0

    def calculateModifiedAttributes(self, fit, runTime, forceProjected = False):
        if forceProjected: return
        for effect in self.item.effects.itervalues():
            if effect.runTime == runTime and effect.isType("passive"):
                effect.handler(fit, self, ("ship",))

    def checkModeItem(self, item):
        """
        Checks if provided item is a valid mode.

        If ship has modes, and current item is not valid, return forced mode
        else if mode is valid, return Mode
        else if ship does not have modes, return None

        @todo: rename this
        """
        items = self.__modeItems

        if items != None:
            if item == None or item not in items:
                # We have a tact dessy, but mode is None or not valid. Force new mode
                return Mode(items[0])
            elif item in items:
                # We have a valid mode
                return Mode(item)
        return None

    @property
    def modeItems(self):
        return self.__modeItems

    @property
    def modes(self):
        return [Mode(item) for item in self.__modeItems] if self.__modeItems else None

    def __getModeItems(self):
        """
        Returns a list of valid mode items for ship. Note that this returns the
        valid Item objects, not the Mode objects. Returns None if not a
        t3 dessy
        """
        if self.item.group.name != "Tactical Destroyer":
            return None

        items = []
        g = eos.db.getGroup("Ship Modifiers", eager=("items.icon", "items.attributes"))
        for item in g.items:
            # Rely on name detection because race is not reliable
            if item.name.lower().startswith(self.item.name.lower()):
                items.append(item)

        return items

    def __deepcopy__(self, memo):
        copy = Ship(self.item)
        return copy
