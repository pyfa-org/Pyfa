"""
Migration 14

- This should take care of issue #586.
"""

import sqlalchemy


def upgrade(saveddata_engine):
    if saveddata_engine.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='fighters'").scalar() == 'fighters':
        # Fighters table exists
        try:
            saveddata_engine.execute("SELECT active FROM fighters LIMIT 1")
        except sqlalchemy.exc.DatabaseError:
            # if we don't have the active column, we are on an old pre-release version. Drop the tables and move on
            # (they will be recreated)

            saveddata_engine.execute("DROP TABLE fighters")
            saveddata_engine.execute("DROP TABLE fightersAbilities")
