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

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relation, mapper, synonym, deferred

from eos.db import gamedata_meta
from eos.gamedata import Icon, Item, MarketGroup

marketgroups_table = Table("invmarketgroups", gamedata_meta,
                           Column("marketGroupID", Integer, primary_key=True),
                           Column("marketGroupName", String),
                           Column("description", String),
                           Column("hasTypes", Boolean),
                           Column("parentGroupID", Integer,
                                  ForeignKey("invmarketgroups.marketGroupID", initially="DEFERRED", deferrable=True)),
                           Column("iconID", Integer, ForeignKey("icons.iconID")))

mapper(MarketGroup, marketgroups_table,
       properties={
           "items"      : relation(Item, backref="marketGroup"),
           "parent"     : relation(MarketGroup, backref="children",
                                   remote_side=[marketgroups_table.c.marketGroupID]),
           "icon"       : relation(Icon),
           "ID"         : synonym("marketGroupID"),
           "name"       : synonym("marketGroupName"),
           "description": deferred(marketgroups_table.c.description)
        })
