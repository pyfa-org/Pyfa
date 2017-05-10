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

from sqlalchemy import Table, Column, Integer, Float, Unicode, ForeignKey, String, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation, mapper, synonym, deferred

from eos.db import gamedata_meta
from eos.gamedata import Attribute, AttributeInfo, Unit, Icon

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
       properties={
           "icon"       : relation(Icon),
           "unit"       : relation(Unit),
           "ID"         : synonym("attributeID"),
           "name"       : synonym("attributeName"),
           "description": deferred(attributes_table.c.description)
       })

Attribute.ID = association_proxy("info", "attributeID")
Attribute.name = association_proxy("info", "attributeName")
Attribute.description = association_proxy("info", "description")
Attribute.published = association_proxy("info", "published")
Attribute.displayName = association_proxy("info", "displayName")
Attribute.highIsGood = association_proxy("info", "highIsGood")
Attribute.iconID = association_proxy("info", "iconID")
Attribute.icon = association_proxy("info", "icon")
Attribute.unit = association_proxy("info", "unit")
