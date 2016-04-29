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
import logging

logger = logging.getLogger(__name__)

class Ship(ItemAttrShortcut, HandledItem):
    EXTRA_ATTRIBUTES = {
        "armorRepair": 0,
        "hullRepair": 0,
        "shieldRepair": 0,
        "maxActiveDrones": 0,
        "maxTargetsLockedFromSkills": 2,
        "droneControlRange": 20000,
        "cloaked": False,
        "siege": False
        # We also have speedLimit for Entosis Link, but there seems to be an
        # issue with naming it exactly "speedLimit" due to unknown reasons.
        # Regardless, we don't have to put it here anyways - it will come up
        # as None unless the Entosis effect sets it.
    }

    def __init__(self, item, parent=None):

        if item.category.name != "Ship":
            raise ValueError('Passed item "%s" (category: (%s)) is not under Ship category'%(item.name, item.category.name))

        self.__item = item
        self.__modeItems = self.__getModeItems()
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = dict(self.item.attributes)
        self.__itemModifiedAttributes.original.update(self.EXTRA_ATTRIBUTES)
        self.__itemModifiedAttributes.overrides = self.item.overrides

        # there are occasions when we need to get to the parent fit of the ship, such as when we need the character
        # skills for ship-role gang boosts (Titans)
        self.parent = parent
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
                # Ships have effects that utilize the level of a skill as an
                # additional operator to the modifier. These are defined in
                # the effect itself, and these skillbooks are registered when
                # they are provided. However, we must re-register the ship
                # before each effect, otherwise effects that do not have
                # skillbook modifiers will use the stale modifier value
                # GH issue #351
                fit.register(self)
                effect.handler(fit, self, ("ship",))

    def validateModeItem(self, item):
        """ Checks if provided item is a valid mode """
        items = self.__modeItems

        if items is not None:
            # if we have items, then we are in a tactical destroyer and must have a mode
            if item is None or item not in items:
                # If provided item is invalid mode, force new one
                return Mode(items[0])
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

    def __repr__(self):
        return "Ship(ID={}, name={}) at {}".format(
            self.item.ID, self.item.name, hex(id(self))
        )
