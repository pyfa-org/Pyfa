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

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import relation, mapper
import datetime

from eos.db import saveddata_meta
from eos.db.saveddata.implant import charImplants_table
from eos.effectHandlerHelpers import HandledImplantBoosterList
from eos.saveddata.implant import Implant
from eos.saveddata.user import User
from eos.saveddata.character import Character, Skill

characters_table = Table("characters", saveddata_meta,
                         Column("ID", Integer, primary_key=True),
                         Column("name", String, nullable=False),
                         Column("apiID", Integer),
                         Column("apiKey", String),
                         Column("defaultChar", Integer),
                         Column("chars", String, nullable=True),
                         Column("defaultLevel", Integer, nullable=True),
                         Column("alphaCloneID", Integer, nullable=True),
                         Column("ownerID", ForeignKey("users.ID"), nullable=True),
                         Column("secStatus", Float, nullable=True, default=0.0),
                         Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                         Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now))

mapper(Character, characters_table,
       properties={
           "_Character__alphaCloneID": characters_table.c.alphaCloneID,
           "savedName"               : characters_table.c.name,
           "_Character__secStatus": characters_table.c.secStatus,
           "_Character__owner"       : relation(
                   User,
                   backref="characters"),
           "_Character__skills"      : relation(
                   Skill,
                   backref="character",
                   cascade="all,delete-orphan"),
           "_Character__implants"    : relation(
                   Implant,
                   collection_class=HandledImplantBoosterList,
                   cascade='all,delete-orphan',
                   backref='character',
                   single_parent=True,
                   primaryjoin=charImplants_table.c.charID == characters_table.c.ID,
                   secondaryjoin=charImplants_table.c.implantID == Implant.ID,
                   secondary=charImplants_table),
       }
       )
