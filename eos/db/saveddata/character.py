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

from eos.db import saveddata_meta
from eos.db.saveddata.implant import charImplants_table
from eos.types import Character, User, Skill, Implant
from eos.effectHandlerHelpers import HandledImplantBoosterList

characters_table = Table("characters", saveddata_meta,
                         Column("ID", Integer, primary_key = True),
                         Column("name", String, nullable = False),
                         Column("apiID", Integer),
                         Column("apiKey", String),
                         Column("defaultLevel", Integer, nullable=True),
                         Column("ownerID", ForeignKey("users.ID"), nullable = True))

mapper(Character, characters_table,
       properties = {"_Character__owner" : relation(User, backref = "characters"),
                     "_Character__skills" : relation(Skill, backref="character", cascade = "all,delete-orphan"),
                     "_Character__implants" : relation(Implant, collection_class = HandledImplantBoosterList, cascade='all,delete-orphan', single_parent=True,
                                                       primaryjoin = charImplants_table.c.charID == characters_table.c.ID,
                                                       secondaryjoin = charImplants_table.c.implantID == Implant.ID,
                                                       secondary = charImplants_table),})
