"""
Migration 16

- Alters fits table to introduce notes attribute
"""

import sqlalchemy


def upgrade(saveddata_engine):
    # Update fits schema to include notes attribute
    try:
        saveddata_engine.execute("SELECT notes FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN notes VARCHAR;")
