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

from sqlalchemy import Table, Column, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import mapper, relation
import datetime

from eos.db import saveddata_meta
from eos.saveddata.booster import Booster
from eos.saveddata.boosterSideEffect import BoosterSideEffect

boosters_table = Table("boosters", saveddata_meta,
                       Column("ID", Integer, primary_key=True),
                       Column("itemID", Integer),
                       Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False),
                       Column("active", Boolean),
                       Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                       Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now),
                       )


booster_side_effect_table = Table("boosterSideEffects", saveddata_meta,
                                  Column("boosterID", Integer, ForeignKey("boosters.ID"), primary_key=True, index=True),
                                  Column("effectID", Integer, nullable=False, primary_key=True),
                                  Column("active", Boolean, default=False)
                                  )


mapper(Booster, boosters_table,
       properties={
        "_Booster__sideEffects": relation(
            BoosterSideEffect,
            backref="booster",
            cascade='all, delete, delete-orphan'),
       }
       )


mapper(BoosterSideEffect, booster_side_effect_table)
