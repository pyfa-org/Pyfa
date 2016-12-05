"""
Migration 13

- Alters fits table to introduce implant location attribute
"""

from sqlalchemy import exc as sqlalchemy_exc


def upgrade(saveddata_engine):
    # Update fits schema to include implant location attribute
    try:
        saveddata_engine.execute("SELECT implantLocation FROM fits LIMIT 1")
    except sqlalchemy_exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN implantLocation INTEGER;")
        saveddata_engine.execute("UPDATE fits SET implantLocation = 0")
