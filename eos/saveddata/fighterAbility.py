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

from sqlalchemy.orm import validates, reconstructor
import logging

logger = logging.getLogger(__name__)

class FighterAbility(object):

    def __init__(self, effect):
        """Initialize from the program"""
        self.__effect = effect
        self.effectID = effect.ID if effect is not None else None
        self.active = False
        self.build()

    @reconstructor
    def init(self):
        '''Initialize from the database'''
        self.__effect = None

        if self.effectID:
            self.__effect = next((x for x in self.fighter.item.effects.itervalues() if x.ID == self.effectID), None)
            if self.__effect is None:
                logger.error("Effect (id: %d) does not exist", self.effectID)
                return

        self.build()

    def build(self):
        pass

    @property
    def effect(self):
        return self.__effect

    @property
    def name(self):
        return self.__effect.getattr('displayName') or self.__effect.handlerName

    @property
    def attrPrefix(self):
        return self.__effect.getattr('prefix')

    @property
    def dealsDamage(self):
        attr = "{}DamageMultiplier".format(self.attrPrefix)
        return attr in self.fighter.itemModifiedAttributes or self.fighter.charge is not None

    @property
    def grouped(self):
        # is the ability applied per fighter (webs, returns False), or as a group (MWD, returned True)
        return self.__effect.getattr('grouped')