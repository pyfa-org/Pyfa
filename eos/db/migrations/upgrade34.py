"""
Migration 34

- Adds projection range columns to projectable entities
"""
import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT projectionRange FROM projectedFits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE projectedFits ADD COLUMN projectionRange FLOAT;")
    try:
        saveddata_engine.execute("SELECT projectionRange FROM modules LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE modules ADD COLUMN projectionRange FLOAT;")
    try:
        saveddata_engine.execute("SELECT projectionRange FROM drones LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE drones ADD COLUMN projectionRange FLOAT;")
    try:
        saveddata_engine.execute("SELECT projectionRange FROM fighters LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fighters ADD COLUMN projectionRange FLOAT;")
