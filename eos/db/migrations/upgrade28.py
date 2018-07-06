"""
Migration 28

- adds baseItemID and mutaplasmidID to modules table
"""
import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT baseItemID FROM modules LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE modules ADD COLUMN baseItemID INT;")

    try:
        saveddata_engine.execute("SELECT mutaplasmidID FROM modules LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE modules ADD COLUMN mutaplasmidID INT;")
