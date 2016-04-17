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
import logging

logger = logging.getLogger(__name__)

class FighterAbility(object):

    def __init__(self, effect):
        print "creating fighter ability"
        """Initialize from the program"""
        self.__effect = effect
        self.effectID = effect.ID if effect is not None else None
        self.active = False
        #self.build()

    @reconstructor
    def init(self):
        '''Initialize from the database'''
        print "Initialize fighter ability from the database, effectID:"
        self.__effect = None
        print self.effectID

        '''
        if self.effectID:
            self.__item = eos.db.getItem(self.itemID)
            if self.__item is None:
                logger.error("Item (id: %d) does not exist", self.itemID)
                return
        '''

        self.build()

    def build(self):
        # pull needed values from effect to here
        pass

    @property
    def effect(self):
        return self.__effect
