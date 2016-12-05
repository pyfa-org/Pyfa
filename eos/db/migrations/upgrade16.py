"""
Migration 16

- Alters fits table to introduce notes attribute
"""

from sqlalchemy import exc as sqlalchemy_exc


def upgrade(saveddata_engine):
    # Update fits schema to include notes attribute
    try:
        saveddata_engine.execute("SELECT notes FROM fits LIMIT 1")
    except sqlalchemy_exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN notes VARCHAR;")
