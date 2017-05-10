"""
Migration 24

- Adds a boolean value to fit to signify if fit should ignore restrictions
"""
import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT ignoreRestrictions FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN ignoreRestrictions BOOLEAN")
        saveddata_engine.execute("UPDATE fits SET ignoreRestrictions = 0")
