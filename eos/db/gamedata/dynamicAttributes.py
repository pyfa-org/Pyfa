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
from sqlalchemy.orm import mapper

from eos.db import gamedata_meta
from eos.gamedata import DynamicItem, DynamicItemAttribute, DynamicItemItem

dynamic_table = Table("mutaplasmids", gamedata_meta,
                          Column("typeID", ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                          Column("resultingTypeID", ForeignKey("invtypes.typeID"), primary_key=True))

dynamicAttributes_table = Table("mutaplasmidAttributes", gamedata_meta,
                      Column("typeID", Integer, ForeignKey("mutaplasmids.typeID"), primary_key=True),
                      Column("attributeID", Integer, primary_key=True),
                      Column("min", Float),
                      Column("max", Float))

dynamicApplicable_table = Table("mutaplasmidItems", gamedata_meta,
                      Column("typeID", Integer, ForeignKey("mutaplasmids.typeID"), primary_key=True),
                      Column("applicableTypeID", ForeignKey("invtypes.typeID"), primary_key=True),
                      )

mapper(DynamicItem, dynamic_table)
mapper(DynamicItemAttribute, dynamicAttributes_table)
mapper(DynamicItemItem, dynamicApplicable_table)
