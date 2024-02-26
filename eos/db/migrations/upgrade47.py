"""
Migration 28

- adds baseItemID and mutaplasmidID to modules table
"""
import sqlalchemy



def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT server FROM ssoCharacter LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE ssoCharacter ADD COLUMN server VARCHAR;")
        saveddata_engine.execute("UPDATE ssoCharacter SET server = 'Tranquility';")



    # update all characters to TQ
