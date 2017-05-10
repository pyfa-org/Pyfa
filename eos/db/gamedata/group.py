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
from eos.gamedata import Category, Group, Icon

groups_table = Table("invgroups", gamedata_meta,
                     Column("groupID", Integer, primary_key=True),
                     Column("groupName", String),
                     Column("description", String),
                     Column("published", Boolean),
                     Column("categoryID", Integer, ForeignKey("invcategories.categoryID")),
                     Column("iconID", Integer, ForeignKey("icons.iconID")))

mapper(Group, groups_table,
       properties={
           "category"   : relation(Category, backref="groups"),
           "icon"       : relation(Icon),
           "ID"         : synonym("groupID"),
           "name"       : synonym("groupName"),
           "description": deferred(groups_table.c.description)
       })
