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

from sqlalchemy import Table, Column, Integer, Float, DateTime
from sqlalchemy.orm import mapper
import datetime

from eos.db import saveddata_meta
from eos.saveddata.override import Override

overrides_table = Table("overrides", saveddata_meta,
                        Column("itemID", Integer, primary_key=True, index=True),
                        Column("attrID", Integer, primary_key=True, index=True),
                        Column("value", Float, nullable=False),
                        Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                        Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now)
                        )

mapper(Override, overrides_table)
