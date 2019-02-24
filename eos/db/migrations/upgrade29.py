"""
Migration 29

- adds spoolType and spoolAmount to modules table
"""
import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT spoolType FROM modules LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE modules ADD COLUMN spoolType INT;")

    try:
        saveddata_engine.execute("SELECT spoolAmount FROM modules LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE modules ADD COLUMN spoolAmount FLOAT;")
