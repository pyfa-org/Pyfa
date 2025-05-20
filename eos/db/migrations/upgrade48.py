"""
Migration 48

- added pilot security column (CONCORD ships)
"""


import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT pilotSecurity FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN pilotSecurity FLOAT")
