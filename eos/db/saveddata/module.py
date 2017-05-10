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

from sqlalchemy import Table, Column, Integer, ForeignKey, CheckConstraint, Boolean, DateTime
from sqlalchemy.orm import relation, mapper
import datetime

from eos.db import saveddata_meta
from eos.saveddata.module import Module
from eos.saveddata.fit import Fit

modules_table = Table("modules", saveddata_meta,
                      Column("ID", Integer, primary_key=True),
                      Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                      Column("itemID", Integer, nullable=True),
                      Column("dummySlot", Integer, nullable=True, default=None),
                      Column("chargeID", Integer),
                      Column("state", Integer, CheckConstraint("state >= -1"), CheckConstraint("state <= 2")),
                      Column("projected", Boolean, default=False, nullable=False),
                      Column("position", Integer),
                      Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                      Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now),
                      CheckConstraint('("dummySlot" = NULL OR "itemID" = NULL) AND "dummySlot" != "itemID"'))

mapper(Module, modules_table,
       properties={"owner": relation(Fit)})
