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

import threading

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import pool

from eos import config
import migration

class ReadOnlyException(Exception):
    pass

gamedata_connectionstring = config.gamedata_connectionstring
if callable(gamedata_connectionstring):
    gamedata_engine = create_engine("sqlite://", creator=gamedata_connectionstring, echo = config.debug)
else:
    gamedata_engine = create_engine(gamedata_connectionstring, echo = config.debug)

gamedata_meta = MetaData()
gamedata_meta.bind = gamedata_engine
gamedata_session = sessionmaker(bind=gamedata_engine, autoflush=False, expire_on_commit=False)()

saveddata_connectionstring = config.saveddata_connectionstring
if saveddata_connectionstring is not None:
    if callable(saveddata_connectionstring):
        saveddata_engine = create_engine(creator=saveddata_connectionstring, echo=config.debug)
    else:
        saveddata_engine = create_engine(saveddata_connectionstring, echo=config.debug)

    saveddata_meta = MetaData()
    saveddata_meta.bind = saveddata_engine
    migration.update(saveddata_engine)
    saveddata_session = sessionmaker(bind=saveddata_engine, autoflush=False, expire_on_commit=False)()

# Lock controlling any changes introduced to session
sd_lock = threading.Lock()

#Import all the definitions for all our database stuff
from eos.db.gamedata import *
from eos.db.saveddata import *

#Import queries
from eos.db.gamedata.queries import getItem, searchItems, getVariations, getItemsByCategory, directAttributeRequest, \
                                    getMarketGroup, getGroup, getCategory, getAttributeInfo, getMetaData, getMetaGroup
from eos.db.saveddata.queries import getUser, getCharacter, getFit, getFitsWithShip, countFitsWithShip, searchFits, \
                                     getCharacterList, getPrice, getDamagePatternList, getDamagePattern, \
                                     getFitList, getFleetList, getFleet, save, remove, commit, add, \
                                     getCharactersForUser, getMiscData, getSquadsIDsWithFitID, getWing, \
                                     getSquad

#If using in memory saveddata, you'll want to reflect it so the data structure is good.
if config.saveddata_connectionstring == "sqlite:///:memory:":
    saveddata_meta.create_all()

def rollback():
    with sd_lock:
        saveddata_session.rollback()
