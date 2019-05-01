"""
Migration 31

- added fit system security column
"""


import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT systemSecurity FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN systemSecurity INT")
