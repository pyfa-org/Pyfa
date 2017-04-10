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

from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import mapper, synonym, deferred

from eos.db import gamedata_meta
from eos.gamedata import Icon

icons_table = Table("icons", gamedata_meta,
                    Column("iconID", Integer, primary_key=True),
                    Column("description", String),
                    Column("iconFile", String))

mapper(Icon, icons_table,
       properties={
           "ID"         : synonym("iconID"),
           "description": deferred(icons_table.c.description)
       })
