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

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relation, mapper
import datetime

from eos.db import saveddata_meta
from eos.db.saveddata.implant import charImplants_table
from eos.effectHandlerHelpers import HandledImplantBoosterList, HandledSsoCharacterList
from eos.saveddata.implant import Implant
from eos.saveddata.user import User
from eos.saveddata.character import Character, Skill
from eos.saveddata.ssocharacter import SsoCharacter

characters_table = Table("characters", saveddata_meta,
                         Column("ID", Integer, primary_key=True),
                         Column("name", String, nullable=False),
                         Column("defaultLevel", Integer, nullable=True),
                         Column("alphaCloneID", Integer, nullable=True),
                         Column("ownerID", ForeignKey("users.ID"), nullable=True),
                         Column("secStatus", Float, nullable=True, default=0.0),
                         Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                         Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now))

sso_table = Table("ssoCharacter", saveddata_meta,
                    Column("ID", Integer, primary_key=True),
                    Column("client", String, nullable=False),
                    Column("characterID", Integer, nullable=False),
                    Column("characterName", String, nullable=False),
                    Column("refreshToken", String, nullable=False),
                    Column("accessToken", String, nullable=False),
                    Column("accessTokenExpires", DateTime, nullable=False),
                    Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                    Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now),
                    UniqueConstraint('client', 'characterID', name='uix_client_characterID'),
                    UniqueConstraint('client', 'characterName', name='uix_client_characterName')
                  )

sso_character_map_table = Table("ssoCharacterMap", saveddata_meta,
                    Column("characterID", ForeignKey("characters.ID"), primary_key=True),
                    Column("ssoCharacterID", ForeignKey("ssoCharacter.ID"), primary_key=True),
                  )


mapper(SsoCharacter, sso_table)

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
           "_Character__ssoCharacters"    : relation(
                   SsoCharacter,
                   collection_class=HandledSsoCharacterList,
                   backref='characters',
                   secondary=sso_character_map_table)
       }
       )
