# ===============================================================================
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
# ===============================================================================

from sqlalchemy.exc import DatabaseError
import logging

logger = logging.getLogger(__name__)


class DatabaseCleanup(object):
    def __init__(self):
        pass

    @staticmethod
    def ExecuteSQLQuery(saveddata_engine, query):
        try:
            results = saveddata_engine.execute(query)
            return results
        except DatabaseError:
            logger.error("Failed to connect to database or error executing query:\n%s", query)
            return None

    @staticmethod
    def OrphanedCharacterSkills(saveddata_engine):
        # Find orphaned character skills.
        # This solves an issue where the character doesn't exist, but skills for that character do.
        # See issue #917
        logger.debug("Running database cleanup for character skills.")
        query = "SELECT COUNT(*) AS num FROM characterSkills WHERE characterID NOT IN (SELECT ID from characters)"
        results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

        if results is None:
            return

        row = results.first()

        if row and row['num']:
            query = "DELETE FROM characterSkills WHERE characterID NOT IN (SELECT ID from characters)"
            delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
            logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

    @staticmethod
    def OrphanedFitDamagePatterns(saveddata_engine):
        # Find orphaned damage patterns.
        # This solves an issue where the damage pattern doesn't exist, but fits reference the pattern.
        # See issue #777
        logger.debug("Running database cleanup for orphaned damage patterns attached to fits.")
        query = "SELECT COUNT(*) AS num FROM fits WHERE damagePatternID NOT IN (SELECT ID FROM damagePatterns) OR damagePatternID IS NULL"
        results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

        if results is None:
            return

        row = results.first()

        if row and row['num']:
            # Get Uniform damage pattern ID
            uniform_query = "SELECT ID FROM damagePatterns WHERE name = 'Uniform'"
            uniform_results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, uniform_query)

            if uniform_results is None:
                return

            rows = uniform_results.fetchall()

            if len(rows) == 0:
                logger.error("Missing uniform damage pattern.")
            elif len(rows) > 1:
                logger.error("More than one uniform damage pattern found.")
            else:
                uniform_damage_pattern_id = rows[0]['ID']
                update_query = "UPDATE 'fits' SET 'damagePatternID' = {} " \
                               "WHERE damagePatternID NOT IN (SELECT ID FROM damagePatterns) OR damagePatternID IS NULL".format(uniform_damage_pattern_id)
                update_results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, update_query)
                logger.error("Database corruption found. Cleaning up %d records.", update_results.rowcount)

    @staticmethod
    def OrphanedFitCharacterIDs(saveddata_engine):
        # Find orphaned character IDs. This solves an issue where the character doesn't exist, but fits reference the pattern.
        logger.debug("Running database cleanup for orphaned characters attached to fits.")
        query = "SELECT COUNT(*) AS num FROM fits WHERE characterID NOT IN (SELECT ID FROM characters) OR characterID IS NULL"
        results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

        if results is None:
            return

        row = results.first()

        if row and row['num']:
            # Get All 5 character ID
            all5_query = "SELECT ID FROM characters WHERE name = 'All 5'"
            all5_results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, all5_query)

            if all5_results is None:
                return

            rows = all5_results.fetchall()

            if len(rows) == 0:
                logger.error("Missing 'All 5' character.")
            elif len(rows) > 1:
                logger.error("More than one 'All 5' character found.")
            else:
                all5_id = rows[0]['ID']
                update_query = "UPDATE 'fits' SET 'characterID' = " + str(all5_id) + \
                               " WHERE characterID not in (select ID from characters) OR characterID IS NULL"
                update_results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, update_query)
                logger.error("Database corruption found. Cleaning up %d records.", update_results.rowcount)

    @staticmethod
    def NullDamagePatternNames(saveddata_engine):
        # Find damage patterns that are missing the name.
        # This solves an issue where the damage pattern ends up with a name that is null.
        # See issue #949
        logger.debug("Running database cleanup for missing damage pattern names.")
        query = "SELECT COUNT(*) AS num FROM damagePatterns WHERE name IS NULL OR name = ''"
        results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

        if results is None:
            return

        row = results.first()

        if row and row['num']:
            query = "DELETE FROM damagePatterns WHERE name IS NULL OR name = ''"
            delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
            logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

    @staticmethod
    def NullTargetResistNames(saveddata_engine):
        # Find target resists that are missing the name.
        # This solves an issue where the target resist ends up with a name that is null.
        # See issue #949
        logger.debug("Running database cleanup for missing target resist names.")
        query = "SELECT COUNT(*) AS num FROM targetResists WHERE name IS NULL OR name = ''"
        results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

        if results is None:
            return

        row = results.first()

        if row and row['num']:
            query = "DELETE FROM targetResists WHERE name IS NULL OR name = ''"
            delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
            logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

    @staticmethod
    def OrphanedFitIDItemID(saveddata_engine):
        # Orphaned items that are missing the fit ID or item ID.
        # See issue #954
        for table in ['drones', 'cargo', 'fighters']:
            logger.debug("Running database cleanup for orphaned %s items.", table)
            query = "SELECT COUNT(*) AS num FROM {} WHERE itemID IS NULL OR itemID = '' or itemID = '0' or fitID IS NULL OR fitID = '' or fitID = '0'".format(
                table)
            results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

            if results is None:
                return

            row = results.first()

            if row and row['num']:
                query = "DELETE FROM {} WHERE itemID IS NULL OR itemID = '' or itemID = '0' or fitID IS NULL OR fitID = '' or fitID = '0'".format(
                    table)
                delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
                logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

        for table in ['modules']:
            logger.debug("Running database cleanup for orphaned %s items.", table)
            query = "SELECT COUNT(*) AS num FROM {} WHERE itemID = '0' or fitID IS NULL OR fitID = '' or fitID = '0'".format(
                table)
            results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

            if results is None:
                return

            row = results.first()

            if row and row['num']:
                query = "DELETE FROM {} WHERE itemID = '0' or fitID IS NULL OR fitID = '' or fitID = '0'".format(table)
                delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
                logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

    @staticmethod
    def NullDamageTargetPatternValues(saveddata_engine):
        # Find patterns that have null values
        # See issue #954
        for profileType in ['damagePatterns', 'targetResists']:
            for damageType in ['em', 'thermal', 'kinetic', 'explosive']:
                logger.debug("Running database cleanup for null %s values. (%s)", profileType, damageType)
                query = "SELECT COUNT(*) AS num FROM {0} WHERE {1}Amount IS NULL OR {1}Amount = ''".format(profileType,
                                                                                                           damageType)
                results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

                if results is None:
                    return

                row = results.first()

                if row and row['num']:
                    query = "UPDATE '{0}' SET '{1}Amount' = '0' WHERE {1}Amount IS NULL OR Amount = ''".format(profileType,
                                                                                                               damageType)
                    delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
                    logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

    @staticmethod
    def DuplicateSelectedAmmoName(saveddata_engine):
        # Orphaned items that are missing the fit ID or item ID.
        # See issue #954
        logger.debug("Running database cleanup for duplicated selected ammo profiles.")
        query = "SELECT COUNT(*) AS num FROM damagePatterns WHERE name = 'Selected Ammo'"
        results = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)

        if results is None:
            return

        row = results.first()

        if row and row['num'] > 1:
            query = "DELETE FROM damagePatterns WHERE name = 'Selected Ammo'"
            delete = DatabaseCleanup.ExecuteSQLQuery(saveddata_engine, query)
            logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)
