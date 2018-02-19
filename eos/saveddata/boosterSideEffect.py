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

from sqlalchemy.orm import reconstructor

pyfalog = Logger(__name__)


class BoosterSideEffect(object):

    def __init__(self, effect):
        """Initialize from the program"""
        self.__effect = effect
        self.effectID = effect.ID if effect is not None else None
        self.active = False
        self.build()

    @reconstructor
    def init(self):
        """Initialize from the database"""
        self.__effect = None

        if self.effectID:
            self.__effect = next((x for x in self.booster.item.effects.values() if x.ID == self.effectID), None)
            if self.__effect is None:
                pyfalog.error("Effect (id: {0}) does not exist", self.effectID)
                return

        self.build()

    def build(self):
        pass

    @property
    def effect(self):
        return self.__effect

    @property
    def name(self):
        return "{0}% {1}".format(
            self.booster.getModifiedItemAttr(self.attr),
            self.__effect.getattr('displayName') or self.__effect.handlerName,
        )

    @property
    def attr(self):
        return self.__effect.getattr('attr')
