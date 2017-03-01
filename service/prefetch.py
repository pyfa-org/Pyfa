# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import os

import config
from eos import db
from eos.db import migration
from eos.db.saveddata.loadDefaultDatabaseValues import DefaultDatabaseValues
from eos.db.saveddata.databaseRepair import DatabaseCleanup

from logbook import Logger

pyfalog = Logger(__name__)

# Make sure the saveddata db exists
if config.savePath and not os.path.exists(config.savePath):
    os.mkdir(config.savePath)

if config.saveDB and os.path.isfile(config.saveDB):
    # If database exists, run migration after init'd database
    pyfalog.debug("Run database migration.")
    db.saveddata_meta.create_all()
    migration.update(db.saveddata_engine)
    # Import default database values
    # Import values that must exist otherwise Pyfa breaks
    pyfalog.debug("Import Required Database Values.")
    DefaultDatabaseValues.importRequiredDefaults()

    # Finds and fixes database corruption issues.
    pyfalog.debug("Starting database validation.")
    database_cleanup_instance = DatabaseCleanup()
    database_cleanup_instance.OrphanedCharacterSkills(db.saveddata_engine)
    database_cleanup_instance.OrphanedFitCharacterIDs(db.saveddata_engine)
    database_cleanup_instance.OrphanedFitDamagePatterns(db.saveddata_engine)
    database_cleanup_instance.NullDamagePatternNames(db.saveddata_engine)
    database_cleanup_instance.NullTargetResistNames(db.saveddata_engine)
    database_cleanup_instance.OrphanedFitIDItemID(db.saveddata_engine)
    database_cleanup_instance.NullDamageTargetPatternValues(db.saveddata_engine)
    database_cleanup_instance.DuplicateSelectedAmmoName(db.saveddata_engine)
    pyfalog.debug("Completed database validation.")

else:
    # If database does not exist, do not worry about migration. Simply
    # create and set version
    pyfalog.debug("Existing database not found, creating new database.")
    db.saveddata_meta.create_all()
    db.saveddata_engine.execute('PRAGMA user_version = {}'.format(migration.getAppVersion()))
    # Import default database values
    # Import values that must exist otherwise Pyfa breaks
    DefaultDatabaseValues.importRequiredDefaults()
    # Import default values for damage profiles
    DefaultDatabaseValues.importDamageProfileDefaults()
    # Import default values for target resist profiles
    DefaultDatabaseValues.importResistProfileDefaults()
