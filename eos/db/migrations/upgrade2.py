"""
Migration 2

- Includes old upgrade paths pre-1.5.0. See GH issue #190 for why this is needed
"""

import sqlalchemy


def upgrade(saveddata_engine):
    # Update characters schema to include default chars
    try:
        saveddata_engine.execute("SELECT defaultChar, chars FROM characters LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE characters ADD COLUMN defaultChar INTEGER")
        saveddata_engine.execute("ALTER TABLE characters ADD COLUMN chars VARCHAR")

    # Update fits schema to include booster attribute
    try:
        saveddata_engine.execute("SELECT booster FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN booster BOOLEAN")
