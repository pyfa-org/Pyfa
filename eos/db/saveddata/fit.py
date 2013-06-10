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
from sqlalchemy.orm import relation, mapper
from sqlalchemy.sql import and_

from eos.db import saveddata_meta
from eos.db.saveddata.module import modules_table
from eos.db.saveddata.drone import drones_table
from eos.db.saveddata.implant import fitImplants_table
from eos.types import Fit, Module, User, Booster, Drone, Implant, Character, DamagePattern
from eos.effectHandlerHelpers import HandledModuleList, HandledDroneList, \
HandledImplantBoosterList, HandledProjectedModList, HandledProjectedDroneList, \
HandledProjectedFitList
fits_table = Table("fits", saveddata_meta,
                         Column("ID", Integer, primary_key = True),
                         Column("ownerID", ForeignKey("users.ID"), nullable = True, index = True),
                         Column("shipID", Integer, nullable = False, index = True),
                         Column("name", String, nullable = False),
                         Column("timestamp", Integer, nullable = False),
                         Column("characterID", ForeignKey("characters.ID"), nullable = True),
                         Column("damagePatternID", ForeignKey("damagePatterns.ID"), nullable=True))

projectedFits_table = Table("projectedFits", saveddata_meta,
                            Column("sourceID", ForeignKey("fits.ID"), primary_key = True),
                            Column("victimID", ForeignKey("fits.ID"), primary_key = True),
                            Column("amount", Integer))
mapper(Fit, fits_table,
       properties = {"_Fit__modules" : relation(Module, collection_class = HandledModuleList,
                                                primaryjoin = and_(modules_table.c.fitID == fits_table.c.ID, modules_table.c.projected == False),
                                                order_by = modules_table.c.position, cascade='all, delete, delete-orphan'),
                     "_Fit__projectedModules" : relation(Module, collection_class = HandledProjectedModList, cascade='all, delete, delete-orphan', single_parent=True,
                                                primaryjoin = and_(modules_table.c.fitID == fits_table.c.ID, modules_table.c.projected == True)),
                     "owner" : relation(User, backref = "fits"),
                     "_Fit__boosters" : relation(Booster, collection_class = HandledImplantBoosterList, cascade='all, delete, delete-orphan', single_parent=True),
                     "_Fit__drones" : relation(Drone, collection_class = HandledDroneList, cascade='all, delete, delete-orphan', single_parent=True,
                                               primaryjoin = and_(drones_table.c.fitID == fits_table.c.ID, drones_table.c.projected == False)),
                     "_Fit__projectedDrones" : relation(Drone, collection_class = HandledProjectedDroneList, cascade='all, delete, delete-orphan', single_parent=True,
                                               primaryjoin = and_(drones_table.c.fitID == fits_table.c.ID, drones_table.c.projected == True)),
                     "_Fit__implants" : relation(Implant, collection_class = HandledImplantBoosterList, cascade='all, delete, delete-orphan', single_parent=True,
                                                 primaryjoin = fitImplants_table.c.fitID == fits_table.c.ID,
                                                 secondaryjoin = fitImplants_table.c.implantID == Implant.ID,
                                                 secondary = fitImplants_table),
                     "_Fit__character" : relation(Character, backref = "fits"),
                     "_Fit__damagePattern" : relation(DamagePattern),
                     "_Fit__projectedFits" : relation(Fit,
                                                      primaryjoin = projectedFits_table.c.victimID == fits_table.c.ID,
                                                      secondaryjoin = fits_table.c.ID == projectedFits_table.c.sourceID,
                                                      secondary = projectedFits_table,
                                                      collection_class = HandledProjectedFitList)
                     })
