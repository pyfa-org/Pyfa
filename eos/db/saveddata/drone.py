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
from sqlalchemy.orm import mapper, relation
import datetime

from eos.db import saveddata_meta
from eos.saveddata.drone import Drone
from eos.saveddata.fit import Fit

drones_table = Table("drones", saveddata_meta,
                     Column("groupID", Integer, primary_key=True),
                     Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                     Column("itemID", Integer, nullable=False),
                     Column("amount", Integer, nullable=False),
                     Column("amountActive", Integer, nullable=False),
                     Column("projected", Boolean, default=False),
                     Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                     Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now)
                     )

mapper(Drone, drones_table,
   properties={
       "owner": relation(Fit)
   }
)
