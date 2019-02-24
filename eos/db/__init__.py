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

import threading

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from . import migration
from eos import config
from logbook import Logger

pyfalog = Logger(__name__)
pyfalog.info("Initializing database")
pyfalog.info("Gamedata connection: {0}", config.gamedata_connectionstring)
pyfalog.info("Saveddata connection: {0}", config.saveddata_connectionstring)

class ReadOnlyException(Exception):
    pass


gamedata_connectionstring = config.gamedata_connectionstring
if callable(gamedata_connectionstring):
    gamedata_engine = create_engine("sqlite://", creator=gamedata_connectionstring, echo=config.debug)
else:
    gamedata_engine = create_engine(gamedata_connectionstring, echo=config.debug)

gamedata_meta = MetaData()
gamedata_meta.bind = gamedata_engine
gamedata_session = sessionmaker(bind=gamedata_engine, autoflush=False, expire_on_commit=False)()

# This should be moved elsewhere, maybe as an actual query. Current, without try-except, it breaks when making a new
# game db because we haven't reached gamedata_meta.create_all()
try:
    config.gamedata_version = gamedata_session.execute(
            "SELECT `field_value` FROM `metadata` WHERE `field_name` LIKE 'client_build'"
    ).fetchone()[0]
    config.gamedata_date = gamedata_session.execute(
        "SELECT `field_value` FROM `metadata` WHERE `field_name` LIKE 'dump_time'"
    ).fetchone()[0]
except Exception as e:
    pyfalog.warning("Missing gamedata version.")
    pyfalog.critical(e)
    config.gamedata_version = None
    config.gamedata_date = None

saveddata_connectionstring = config.saveddata_connectionstring
if saveddata_connectionstring is not None:
    if callable(saveddata_connectionstring):
        saveddata_engine = create_engine(creator=saveddata_connectionstring, echo=config.debug)
    else:
        saveddata_engine = create_engine(saveddata_connectionstring, echo=config.debug)

    saveddata_meta = MetaData()
    saveddata_meta.bind = saveddata_engine
    saveddata_session = sessionmaker(bind=saveddata_engine, autoflush=False, expire_on_commit=False)()
else:
    saveddata_meta = None

# Lock controlling any changes introduced to session
sd_lock = threading.RLock()

# Import all the definitions for all our database stuff
# noinspection PyPep8
from eos.db.gamedata import alphaClones, attribute, category, effect, group, item, marketGroup, metaData, metaGroup, queries, traits, unit, dynamicAttributes
# noinspection PyPep8
from eos.db.saveddata import booster, cargo, character, damagePattern, databaseRepair, drone, fighter, fit, implant, implantSet, loadDefaultDatabaseValues, \
    miscData, mutator, module, override, price, queries, skill, targetResists, user

# Import queries
# noinspection PyPep8
from eos.db.gamedata.queries import *
# noinspection PyPep8
from eos.db.saveddata.queries import *

# If using in memory saveddata, you'll want to reflect it so the data structure is good.
if config.saveddata_connectionstring == "sqlite:///:memory:":
    saveddata_meta.create_all()
    pyfalog.info("Running database out of memory.")


def rollback():
    with sd_lock:
        pyfalog.warning("Session rollback triggered.")
        saveddata_session.rollback()
