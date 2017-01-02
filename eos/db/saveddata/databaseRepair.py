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

import sqlalchemy
import logging

logger = logging.getLogger(__name__)


class DatabaseCleanup:
    def __init__(self):
        pass

    @staticmethod
    def OrphanedCharacterSkills(saveddata_engine):
        # Finds and fixes database corruption issues.
        logger.debug("Start databsae validation and cleanup.")

        # Find orphaned character skills.
        # This solves an issue where the character doesn't exist, but skills for that character do.
        # See issue #917
        try:
            logger.debug("Running database cleanup for character skills.")
            results = saveddata_engine.execute("SELECT COUNT(*) AS num FROM characterSkills "
                                               "WHERE characterID NOT IN (SELECT ID from characters)")

            if results.fetchone()['num'] > 0:
                delete = saveddata_engine.execute("DELETE FROM characterSkills WHERE characterID NOT IN (SELECT ID from characters)")
                logger.error("Database corruption found. Cleaning up %d records.", delete.rowcount)

        except sqlalchemy.exc.DatabaseError:
            logger.error("Failed to connect to database.")

    @staticmethod
    def OrphanedFitDamagePatterns(saveddata_engine):
        # Find orphaned damage patterns.
        # This solves an issue where the damage pattern doesn't exist, but fits reference the pattern.
        # See issue #777
        try:
            logger.debug("Running database cleanup for orphaned damage patterns attached to fits.")
            results = saveddata_engine.execute("SELECT COUNT(*) AS num FROM fits WHERE damagePatternID not in (select ID from damagePatterns)")

            if results.fetchone()['num'] > 0:
                # Get Uniform damage pattern ID
                uniform_results = saveddata_engine.execute("select ID from damagePatterns WHERE name = 'Uniform'")

                uniform_result_count = 0
                uniform_damage_pattern_id = 0
                for uniform_result in uniform_results:
                    uniform_damage_pattern_id = uniform_result[0]
                    uniform_result_count += 1

                if uniform_result_count == 0:
                    logger.error("Missing uniform damage pattern.")
                elif uniform_result_count > 1:
                    logger.error("More than one uniform damage pattern found.")
                else:
                    update = saveddata_engine.execute("UPDATE 'fits' SET 'damagePatternID' = ? "
                                             "WHERE damagePatternID NOT IN (SELECT ID FROM damagePatterns)",
                                             uniform_damage_pattern_id)
                    logger.error("Database corruption found. Cleaning up %d records.", update.rowcount)
        except sqlalchemy.exc.DatabaseError:
            logger.error("Failed to connect to database.")

    @staticmethod
    def OrphanedFitCharacterIDs(saveddata_engine):
        # Find orphaned character IDs. This solves an issue where the chaaracter doesn't exist, but fits reference the pattern.
        try:
            logger.debug("Running database cleanup for orphaned characters attached to fits.")
            results = saveddata_engine.execute("SELECT COUNT(*) AS num FROM fits WHERE characterID NOT IN (SELECT ID FROM characters)")

            # Count how many records exist.  This is ugly, but SQLAlchemy doesn't return a count from a select query.
            if results.fetchone()['num'] > 0:
                # Get All 5 character ID
                all5_results = saveddata_engine.execute("SELECT ID FROM characters WHERE name = 'All 5'")

                all5_result_count = 0
                all5_id = 0
                for all5_result in all5_results:
                    all5_id = all5_result[0]
                    all5_result_count += 1

                if all5_result_count == 0:
                    logger.error("Missing 'All 5' character.")
                elif all5_result_count > 1:
                    logger.error("More than one 'All 5' character found.")
                else:
                    update = saveddata_engine.execute("UPDATE 'fits' SET 'damagePatternID' = ? "
                                             "WHERE damagePatternID not in (select ID from damagePatterns)",
                                             all5_id)
                    logger.error("Database corruption found. Cleaning up %d records.", update.rowcount)
        except sqlalchemy.exc.DatabaseError:
            logger.error("Failed to connect to database.")
