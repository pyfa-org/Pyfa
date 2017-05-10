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

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation, mapper, synonym

from eos.db import gamedata_meta
from eos.db.gamedata.item import items_table
from eos.gamedata import Item, MetaGroup, MetaType

metagroups_table = Table("invmetagroups", gamedata_meta,
                         Column("metaGroupID", Integer, primary_key=True),
                         Column("metaGroupName", String))

metatypes_table = Table("invmetatypes", gamedata_meta,
                        Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                        Column("parentTypeID", Integer, ForeignKey("invtypes.typeID")),
                        Column("metaGroupID", Integer, ForeignKey("invmetagroups.metaGroupID")))

mapper(MetaGroup, metagroups_table,
       properties={
           "ID"  : synonym("metaGroupID"),
           "name": synonym("metaGroupName")
        })

mapper(MetaType, metatypes_table,
       properties={
           "ID"    : synonym("metaGroupID"),
           "parent": relation(Item, primaryjoin=metatypes_table.c.parentTypeID == items_table.c.typeID),
           "items" : relation(Item, primaryjoin=metatypes_table.c.typeID == items_table.c.typeID),
           "info"  : relation(MetaGroup, lazy=False)
        })

MetaType.name = association_proxy("info", "name")
