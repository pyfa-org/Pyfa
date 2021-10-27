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

from sqlalchemy import Table, Column, Integer, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import mapper, relation, synonym
from sqlalchemy.orm.collections import attribute_mapped_collection
import datetime

from eos.db import saveddata_meta
from eos.saveddata.drone import Drone
from eos.saveddata.fit import Fit
from eos.saveddata.mutator import MutatorDrone

drones_table = Table("drones", saveddata_meta,
                     Column("groupID", Integer, primary_key=True),
                     Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                     Column("itemID", Integer, nullable=False),
                     Column("baseItemID", Integer, nullable=True),
                     Column("mutaplasmidID", Integer, nullable=True),
                     Column("amount", Integer, nullable=False),
                     Column("amountActive", Integer, nullable=False),
                     Column("projected", Boolean, default=False),
                     Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                     Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now),
                     Column("projectionRange", Float, nullable=True))


mapper(Drone, drones_table,
   properties={
       "ID": synonym("groupID"),
       "owner": relation(Fit),
       "mutators": relation(
               MutatorDrone,
               backref="item",
               cascade="all,delete-orphan",
               collection_class=attribute_mapped_collection('attrID'))})
