# ===============================================================================
# Copyright (C) 2015 Ryan Holmes
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

import eos.db
from eos.eqBase import EqBase

pyfalog = Logger(__name__)


class Override(EqBase):
    def __init__(self, item, attr, value):
        self.itemID = item.ID
        self.__item = item
        self.attrID = attr.ID
        self.__attr = attr
        self.value = value

    @reconstructor
    def init(self):
        self.__attr = None
        self.__item = None

        if self.attrID:
            self.__attr = eos.db.getAttributeInfo(self.attrID)
            if self.__attr is None:
                pyfalog.error("Attribute (id: {0}) does not exist", self.attrID)
                return

        if self.itemID:
            self.__item = eos.db.getItem(self.itemID)
            if self.__item is None:
                pyfalog.error("Item (id: {0}) does not exist", self.itemID)
                return

    @property
    def attr(self):
        return self.__attr

    @property
    def item(self):
        return self.__item
