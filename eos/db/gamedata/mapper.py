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

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Table
from sqlalchemy import Float
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation, mapper, synonym, deferred
from sqlalchemy.orm.collections import attribute_mapped_collection

from eos.db import gamedata_meta
from eos.gamedata import Attribute, Effect, Group
from eos.gamedata import AttributeInfo
from eos.gamedata import Category, Icon
from eos.gamedata import EffectInfo
from eos.gamedata import Item, MetaGroup, MetaType
from eos.gamedata import MarketGroup
from eos.gamedata import MetaData
from eos.gamedata import Traits
from eos.gamedata import Unit

typeattributes_table = Table("dgmtypeattribs", gamedata_meta,
                             Column("value", Float),
                             Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                             Column("attributeID", ForeignKey("dgmattribs.attributeID"), primary_key=True))

attributes_table = Table("dgmattribs", gamedata_meta,
                         Column("attributeID", Integer, primary_key=True),
                         Column("attributeName", String),
                         Column("defaultValue", Float),
                         Column("maxAttributeID", Integer, ForeignKey("dgmattribs.attributeID")),
                         Column("description", Unicode),
                         Column("published", Boolean),
                         Column("displayName", String),
                         Column("highIsGood", Boolean),
                         Column("iconID", Integer, ForeignKey("icons.iconID")),
                         Column("unitID", Integer, ForeignKey("dgmunits.unitID")))

mapper(Attribute, typeattributes_table,
       properties={"info": relation(AttributeInfo, lazy=False)})

mapper(AttributeInfo, attributes_table,
       properties={"icon": relation(Icon),
                   "unit": relation(Unit),
                   "ID": synonym("attributeID"),
                   "name": synonym("attributeName"),
                   "description": deferred(attributes_table.c.description)})

Attribute.ID = association_proxy("info", "attributeID")
Attribute.name = association_proxy("info", "attributeName")
Attribute.description = association_proxy("info", "description")
Attribute.published = association_proxy("info", "published")
Attribute.displayName = association_proxy("info", "displayName")
Attribute.highIsGood = association_proxy("info", "highIsGood")
Attribute.iconID = association_proxy("info", "iconID")
Attribute.icon = association_proxy("info", "icon")
Attribute.unit = association_proxy("info", "unit")

categories_table = Table("invcategories", gamedata_meta,
                         Column("categoryID", Integer, primary_key=True),
                         Column("categoryName", String),
                         Column("description", String),
                         Column("published", Boolean),
                         Column("iconID", Integer, ForeignKey("icons.iconID")))

mapper(Category, categories_table,
       properties={"icon": relation(Icon),
                   "ID": synonym("categoryID"),
                   "name": synonym("categoryName"),
                   "description": deferred(categories_table.c.description)})

Effect.name = association_proxy("info", "name")
Effect.description = association_proxy("info", "description")
Effect.published = association_proxy("info", "published")

traits_table = Table("invtraits", gamedata_meta,
                     Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                     Column("traitText", String))

mapper(Traits, traits_table)

typeeffects_table = Table("dgmtypeeffects", gamedata_meta,
                          Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                          Column("effectID", Integer, ForeignKey("dgmeffects.effectID"), primary_key=True))

effects_table = Table("dgmeffects", gamedata_meta,
                      Column("effectID", Integer, primary_key=True),
                      Column("effectName", String),
                      Column("description", String),
                      Column("published", Boolean),
                      Column("isAssistance", Boolean),
                      Column("isOffensive", Boolean))

mapper(EffectInfo, effects_table,
       properties={"ID": synonym("effectID"),
                   "name": synonym("effectName"),
                   "description": deferred(effects_table.c.description)})

mapper(Effect, typeeffects_table,
       properties={"ID": synonym("effectID"),
                   "info": relation(EffectInfo, lazy=False)})

groups_table = Table("invgroups", gamedata_meta,
                     Column("groupID", Integer, primary_key=True),
                     Column("groupName", String),
                     Column("description", String),
                     Column("published", Boolean),
                     Column("categoryID", Integer, ForeignKey("invcategories.categoryID")),
                     Column("iconID", Integer, ForeignKey("icons.iconID")))

mapper(Group, groups_table,
       properties={"category": relation(Category, backref="groups"),
                   "icon": relation(Icon),
                   "ID": synonym("groupID"),
                   "name": synonym("groupName"),
                   "description": deferred(groups_table.c.description)})

icons_table = Table("icons", gamedata_meta,
                    Column("iconID", Integer, primary_key=True),
                    Column("description", String),
                    Column("iconFile", String))

mapper(Icon, icons_table,
       properties={"ID": synonym("iconID"),
                   "description": deferred(icons_table.c.description)})

metagroups_table = Table("invmetagroups", gamedata_meta,
                         Column("metaGroupID", Integer, primary_key=True),
                         Column("metaGroupName", String))

metatypes_table = Table("invmetatypes", gamedata_meta,
                        Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                        Column("parentTypeID", Integer, ForeignKey("invtypes.typeID")),
                        Column("metaGroupID", Integer, ForeignKey("invmetagroups.metaGroupID")))

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

mapper(Item, items_table,
       properties={"group": relation(Group, backref="items"),
                   "icon": relation(Icon),
                   "_Item__attributes": relation(Attribute, collection_class=attribute_mapped_collection('name')),
                   "effects": relation(Effect, collection_class=attribute_mapped_collection('name')),
                   "metaGroup": relation(MetaType,
                                         primaryjoin=metatypes_table.c.typeID == items_table.c.typeID,
                                         uselist=False),
                   "ID": synonym("typeID"),
                   "name": synonym("typeName"),
                   "description": deferred(items_table.c.description),
                   "traits": relation(Traits,
                                      primaryjoin=traits_table.c.typeID == items_table.c.typeID,
                                      uselist=False)
                   })

Item.category = association_proxy("group", "category")

mapper(MetaGroup, metagroups_table,
       properties={"ID": synonym("metaGroupID"),
                   "name": synonym("metaGroupName")})

mapper(MetaType, metatypes_table,
       properties={"ID": synonym("metaGroupID"),
                   "parent": relation(Item, primaryjoin=metatypes_table.c.parentTypeID == items_table.c.typeID),
                   "items": relation(Item, primaryjoin=metatypes_table.c.typeID == items_table.c.typeID),
                   "info": relation(MetaGroup, lazy=False)})

MetaType.name = association_proxy("info", "name")

marketgroups_table = Table("invmarketgroups", gamedata_meta,
                           Column("marketGroupID", Integer, primary_key=True),
                           Column("marketGroupName", String),
                           Column("description", String),
                           Column("hasTypes", Boolean),
                           Column("parentGroupID", Integer,
                                  ForeignKey("invmarketgroups.marketGroupID", initially="DEFERRED", deferrable=True)),
                           Column("iconID", Integer, ForeignKey("icons.iconID")))

mapper(MarketGroup, marketgroups_table,
       properties={"items": relation(Item, backref="marketGroup"),
                   "parent": relation(MarketGroup, backref="children",
                                      remote_side=[marketgroups_table.c.marketGroupID]),
                   "icon": relation(Icon),
                   "ID": synonym("marketGroupID"),
                   "name": synonym("marketGroupName"),
                   "description": deferred(marketgroups_table.c.description)})

metadata_table = Table("metadata", gamedata_meta,
                       Column("field_name", String, primary_key=True),
                       Column("field_value", String))

mapper(MetaData, metadata_table)

groups_table = Table("dgmunits", gamedata_meta,
                     Column("unitID", Integer, primary_key=True),
                     Column("unitName", String),
                     Column("displayName", String))

mapper(Unit, groups_table,
       properties={"ID": synonym("unitID"),
                   "name": synonym("unitName")})
