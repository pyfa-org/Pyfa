"""
Migration 32

- added speed, sig and radius columns to targetResists table
"""


import sqlalchemy


def upgrade(saveddata_engine):
    for column in ('maxVelocity', 'signatureRadius', 'radius'):
        try:
            saveddata_engine.execute("SELECT {} FROM targetResists LIMIT 1;".format(column))
        except sqlalchemy.exc.DatabaseError:
            saveddata_engine.execute("ALTER TABLE targetResists ADD COLUMN {} FLOAT;".format(column))
