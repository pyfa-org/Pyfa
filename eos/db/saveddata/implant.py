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

from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapper
import datetime

from eos.db import saveddata_meta
from eos.saveddata.implant import Implant

implants_table = Table("implants", saveddata_meta,
                       Column("ID", Integer, primary_key=True),
                       Column("itemID", Integer),
                       Column("active", Boolean),
                       Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                       Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now)
                       )

fitImplants_table = Table("fitImplants", saveddata_meta,
                          Column("fitID", ForeignKey("fits.ID"), index=True),
                          Column("implantID", ForeignKey("implants.ID"), primary_key=True))

charImplants_table = Table("charImplants", saveddata_meta,
                           Column("charID", ForeignKey("characters.ID"), index=True),
                           Column("implantID", ForeignKey("implants.ID"), primary_key=True))

implantsSetMap_table = Table("implantSetMap", saveddata_meta,
                             Column("setID", ForeignKey("implantSets.ID"), index=True),
                             Column("implantID", ForeignKey("implants.ID"), primary_key=True))

mapper(Implant, implants_table)
