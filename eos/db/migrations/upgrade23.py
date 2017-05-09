"""
Migration 23

- Adds a sec status field to the character table
"""
import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT secStatus FROM characters LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE characters ADD COLUMN secStatus FLOAT;")
