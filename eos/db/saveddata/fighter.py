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
from eos.saveddata.fighterAbility import FighterAbility
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit

fighters_table = Table("fighters", saveddata_meta,
                       Column("groupID", Integer, primary_key=True),
                       Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                       Column("itemID", Integer, nullable=False),
                       Column("active", Boolean, nullable=True),
                       Column("amount", Integer, nullable=False),
                       Column("projected", Boolean, default=False),
                       Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                       Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now)
                       )

fighter_abilities_table = Table("fightersAbilities", saveddata_meta,
                                Column("groupID", Integer, ForeignKey("fighters.groupID"), primary_key=True,
                                       index=True),
                                Column("effectID", Integer, nullable=False, primary_key=True),
                                Column("active", Boolean, default=False))

mapper(Fighter, fighters_table,
       properties={
           "owner"              : relation(Fit),
           "_Fighter__abilities": relation(
                   FighterAbility,
                   backref="fighter",
                   cascade='all, delete, delete-orphan'),
       })

mapper(FighterAbility, fighter_abilities_table)
