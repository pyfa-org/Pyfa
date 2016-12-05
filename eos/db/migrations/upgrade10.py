"""
Migration 10

- Adds active attribute to projected fits
"""

from sqlalchemy import exc as sqlalchemy_exc


def upgrade(saveddata_engine):
    # Update projectedFits schema to include active attribute
    try:
        saveddata_engine.execute("SELECT active FROM projectedFits LIMIT 1")
    except sqlalchemy_exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE projectedFits ADD COLUMN active BOOLEAN")
        saveddata_engine.execute("UPDATE projectedFits SET active = 1")
        saveddata_engine.execute("UPDATE projectedFits SET amount = 1")
