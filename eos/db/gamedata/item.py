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

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Float
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation, mapper, synonym, deferred
from sqlalchemy.orm.collections import attribute_mapped_collection
from eos.db.gamedata.effect import typeeffects_table

from eos.db import gamedata_meta
from eos.gamedata import Attribute, Effect, Group, Icon, Item, MetaType, Traits

items_table = Table("invtypes", gamedata_meta,
                    Column("typeID", Integer, primary_key=True),
                    Column("typeName", String, index=True),
                    Column("description", String),
                    Column("raceID", Integer),
                    Column("factionID", Integer),
                    Column("volume", Float),
                    Column("mass", Float),
                    Column("capacity", Float),
                    Column("published", Boolean),
                    Column("marketGroupID", Integer, ForeignKey("invmarketgroups.marketGroupID")),
                    Column("iconID", Integer, ForeignKey("icons.iconID")),
                    Column("groupID", Integer, ForeignKey("invgroups.groupID"), index=True))

from .metaGroup import metatypes_table  # noqa
from .traits import traits_table  # noqa

mapper(Item, items_table,
       properties={
           "group"            : relation(Group, backref="items"),
           "icon"             : relation(Icon),
           "_Item__attributes": relation(Attribute, cascade='all, delete, delete-orphan', collection_class=attribute_mapped_collection('name')),
           "effects": relation(Effect, secondary=typeeffects_table, collection_class=attribute_mapped_collection('name')),
           "metaGroup"        : relation(MetaType,
                                         primaryjoin=metatypes_table.c.typeID == items_table.c.typeID,
                                         uselist=False),
           "ID"               : synonym("typeID"),
           "name"             : synonym("typeName"),
           "description"      : deferred(items_table.c.description),
           "traits"           : relation(Traits,
                                         primaryjoin=traits_table.c.typeID == items_table.c.typeID,
                                         uselist=False)
       })

Item.category = association_proxy("group", "category")
