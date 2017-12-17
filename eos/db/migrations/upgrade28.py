"""
Migration 28

- Adds the signatureRadius and maxVelocity fields to TargetResists
"""
import sqlalchemy


def upgrade(saveddata_engine):
    for column in ('signatureRadius','maxVelocity'):
        try:
            saveddata_engine.execute("SELECT {} FROM targetResists LIMIT 1;".format(column))
        except sqlalchemy.exc.DatabaseError:
            saveddata_engine.execute("ALTER TABLE targetResists ADD COLUMN {} FLOAT;".format(column))
