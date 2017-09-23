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

from sqlalchemy import Table, Column, Float, Integer
from sqlalchemy.orm import mapper

from eos.db import saveddata_meta
from eos.saveddata.price import Price

prices_table = Table("prices", saveddata_meta,
                     Column("typeID", Integer, primary_key=True),
                     Column("price", Float, default=0.0),
                     Column("time", Integer, nullable=False),
                     Column("failed", Integer))

mapper(Price, prices_table, properties={
    "_Price__price": prices_table.c.price,
})
