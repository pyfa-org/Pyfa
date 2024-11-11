"""
Migration 49

- added hp column to targetResists table
"""


import sqlalchemy


def upgrade(saveddata_engine):
        try:
            saveddata_engine.execute("SELECT hp FROM targetResists LIMIT 1;")
        except sqlalchemy.exc.DatabaseError:
            saveddata_engine.execute("ALTER TABLE targetResists ADD COLUMN hp FLOAT;")
