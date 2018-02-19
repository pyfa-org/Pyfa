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

from eos.effectHandlerHelpers import HandledItem
from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut


class Mode(ItemAttrShortcut, HandledItem):
    def __init__(self, item):

        if item.group.name != "Ship Modifiers":
            raise ValueError(
                    'Passed item "%s" (category: (%s)) is not a Ship Modifier' % (item.name, item.category.name))

        self.__item = item
        self.__itemModifiedAttributes = ModifiedAttributeDict()
        self.__itemModifiedAttributes.original = self.item.attributes
        self.__itemModifiedAttributes.overrides = self.item.overrides

    @property
    def item(self):
        return self.__item

    @property
    def itemModifiedAttributes(self):
        return self.__itemModifiedAttributes

    # @todo: rework to fit only on t3 dessy
    def fits(self, fit):
        raise NotImplementedError()

    def clear(self):
        self.itemModifiedAttributes.clear()

    def calculateModifiedAttributes(self, fit, runTime, forceProjected=False):
        if self.item:
            for effect in self.item.effects.values():
                if effect.runTime == runTime and effect.activeByDefault:
                    effect.handler(fit, self, context=("module",))
