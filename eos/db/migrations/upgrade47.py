"""
Migration 46

- add support for server selection for SSO characters
"""
import sqlalchemy

tmpTable = """
    CREATE TABLE ssoCharacterTemp (
        ID INTEGER NOT NULL, 
        client VARCHAR NOT NULL, 
        characterID INTEGER NOT NULL, 
        characterName VARCHAR NOT NULL, 
        refreshToken VARCHAR NOT NULL, 
        accessToken VARCHAR NOT NULL, 
        accessTokenExpires DATETIME NOT NULL, 
        created DATETIME, 
        modified DATETIME,
        server VARCHAR, 
        PRIMARY KEY (ID), 
        CONSTRAINT "uix_client_server_characterID" UNIQUE (client, server, characterID), 
        CONSTRAINT "uix_client_server_characterName" UNIQUE (client, server, characterName)
    )
"""

def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT server FROM ssoCharacter LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute(tmpTable)
        saveddata_engine.execute(
            "INSERT INTO ssoCharacterTemp (ID, client, characterID, characterName, refreshToken, accessToken, accessTokenExpires, created, modified, server) "
            "SELECT ID, client, characterID, characterName, refreshToken, accessToken, accessTokenExpires, created, modified, 'Tranquility' "
            "FROM ssoCharacter")
        saveddata_engine.execute("DROP TABLE ssoCharacter")
        saveddata_engine.execute("ALTER TABLE ssoCharacterTemp RENAME TO ssoCharacter")
