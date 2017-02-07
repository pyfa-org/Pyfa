"""
Migration 20

- Adds support for alpha clones to the characters table
"""

import sqlalchemy


def upgrade(saveddata_engine):
    # Update characters schema to include alphaCloneID
    try:
        saveddata_engine.execute("SELECT alphaCloneID FROM characters LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE characters ADD COLUMN alphaCloneID INTEGER;")
