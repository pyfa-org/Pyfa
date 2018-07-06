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

from sqlalchemy import Column, Float, Integer, Table, ForeignKey
from sqlalchemy.orm import mapper, relation, synonym
from sqlalchemy.ext.associationproxy import association_proxy

from eos.db import gamedata_meta
from eos.gamedata import DynamicItem, DynamicItemAttribute, DynamicItemItem, Item

from eos.gamedata import AttributeInfo

dynamic_table = Table("mutaplasmids", gamedata_meta,
                          Column("typeID", ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                          Column("resultingTypeID", ForeignKey("invtypes.typeID"), primary_key=True))

dynamicAttributes_table = Table("mutaplasmidAttributes", gamedata_meta,
                      Column("typeID", Integer, ForeignKey("mutaplasmids.typeID"), primary_key=True),
                      Column("attributeID", ForeignKey("dgmattribs.attributeID"), primary_key=True),
                      Column("min", Float),
                      Column("max", Float))

dynamicApplicable_table = Table("mutaplasmidItems", gamedata_meta,
                      Column("typeID", ForeignKey("mutaplasmids.typeID"), primary_key=True),
                      Column("applicableTypeID", ForeignKey("invtypes.typeID"), primary_key=True),
                      )

mapper(DynamicItem, dynamic_table, properties={
           "attributes": relation(DynamicItemAttribute),
           "item": relation(Item, foreign_keys=[dynamic_table.c.typeID]),
           "resultingItem": relation(Item, foreign_keys=[dynamic_table.c.resultingTypeID]),
           "ID": synonym("typeID"),
})

mapper(DynamicItemAttribute, dynamicAttributes_table,
       properties={"info": relation(AttributeInfo, lazy=False)})

mapper(DynamicItemItem, dynamicApplicable_table, properties={
           "mutaplasmid": relation(DynamicItem),
       })

DynamicItemAttribute.ID = association_proxy("info", "attributeID")
DynamicItemAttribute.name = association_proxy("info", "attributeName")
DynamicItemAttribute.description = association_proxy("info", "description")
DynamicItemAttribute.published = association_proxy("info", "published")
DynamicItemAttribute.displayName = association_proxy("info", "displayName")
DynamicItemAttribute.highIsGood = association_proxy("info", "highIsGood")
DynamicItemAttribute.iconID = association_proxy("info", "iconID")
DynamicItemAttribute.icon = association_proxy("info", "icon")
DynamicItemAttribute.unit = association_proxy("info", "unit")
