"""
Migration 30

- changes to prices table
"""


import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT status FROM prices LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        # Just drop table, table will be re-created by sqlalchemy and
        # data will be re-fetched
        saveddata_engine.execute("DROP TABLE prices;")
