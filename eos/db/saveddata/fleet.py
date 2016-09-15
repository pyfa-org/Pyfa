#===============================================================================
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
#===============================================================================

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import mapper, relation

from eos.db import saveddata_meta
from eos.types import Fleet, Wing, Squad, Fit
from eos.db.saveddata.fit import fits_table

gangs_table = Table("gangs", saveddata_meta,
                    Column("ID", Integer, primary_key = True),
                    Column("leaderID", ForeignKey("fits.ID")),
                    Column("boosterID", ForeignKey("fits.ID")),
                    Column("name", String))

wings_table = Table("wings", saveddata_meta,
                    Column("ID", Integer, primary_key = True),
                    Column("gangID", ForeignKey("gangs.ID")),
                    Column("boosterID", ForeignKey("fits.ID")),
                    Column("leaderID", ForeignKey("fits.ID")))

squads_table = Table("squads", saveddata_meta,
                     Column("ID", Integer, primary_key = True),
                     Column("wingID", ForeignKey("wings.ID")),
                     Column("leaderID", ForeignKey("fits.ID")),
                     Column("boosterID", ForeignKey("fits.ID")))

squadmembers_table = Table("squadmembers", saveddata_meta,
                           Column("squadID", ForeignKey("squads.ID"), primary_key = True),
                           Column("memberID", ForeignKey("fits.ID"), primary_key = True))

mapper(Fleet, gangs_table,
       properties = {"wings" : relation(Wing, backref="gang"),
                     "leader" : relation(Fit, primaryjoin = gangs_table.c.leaderID == fits_table.c.ID),
                     "booster": relation(Fit, primaryjoin = gangs_table.c.boosterID == fits_table.c.ID)})

mapper(Wing, wings_table,
       properties = {"squads" : relation(Squad, backref="wing"),
                     "leader" : relation(Fit, primaryjoin = wings_table.c.leaderID == fits_table.c.ID),
                     "booster": relation(Fit, primaryjoin = wings_table.c.boosterID == fits_table.c.ID)})

mapper(Squad, squads_table,
       properties = {"leader" : relation(Fit, primaryjoin = squads_table.c.leaderID == fits_table.c.ID),
                     "booster" : relation(Fit, primaryjoin = squads_table.c.boosterID == fits_table.c.ID),
                     "members" : relation(Fit,
                                          primaryjoin = squads_table.c.ID == squadmembers_table.c.squadID,
                                          secondaryjoin = squadmembers_table.c.memberID == fits_table.c.ID,
                                          secondary = squadmembers_table)})

