"""
Migration 45

- Drone mutaplasmid support
"""

import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT baseItemID FROM drones LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE drones ADD COLUMN baseItemID INTEGER;")
    try:
        saveddata_engine.execute("SELECT mutaplasmidID FROM drones LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE drones ADD COLUMN mutaplasmidID INTEGER;")
