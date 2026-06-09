"""
Migration 50

- add pulseInterval column to modules table
"""

import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT pulseInterval FROM modules LIMIT 1;")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE modules ADD COLUMN pulseInterval FLOAT;")
