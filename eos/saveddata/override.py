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

import logging

from sqlalchemy.orm import reconstructor

from eos.eqBase import EqBase
from eos.db import saveddata_session, sd_lock

from eos.db.saveddata import queries as eds_queries

logger = logging.getLogger(__name__)


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
            self.__attr = edg_queries.getAttributeInfo(self.attrID)
            if self.__attr is None:
                logger.error("Attribute (id: %d) does not exist", self.attrID)
                return

        if self.itemID:
            self.__item = edg_queries.getItem(self.itemID)
            if self.__item is None:
                logger.error("Item (id: %d) does not exist", self.itemID)
                return

    @property
    def attr(self):
        return self.__attr

    @property
    def item(self):
        return self.__item


def getOverrides(itemID, eager=None):
    if isinstance(itemID, int):
        return saveddata_session.query(Override).filter(Override.itemID == itemID).all()
    else:
        raise TypeError("Need integer as argument")


def clearOverrides():
    with sd_lock:
        deleted_rows = saveddata_session.query(Override).delete()
    eds_queries.commit()
    return deleted_rows


def getAllOverrides(eager=None):
    return saveddata_session.query(Override).all()
