"""
Migration 50

- added commandLinks table (generic / virtual command links)
"""

import sqlalchemy


def upgrade(saveddata_engine):
    try:
        saveddata_engine.execute("SELECT ID FROM commandLinks LIMIT 1;")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("""
            CREATE TABLE commandLinks (
                ID INTEGER NOT NULL PRIMARY KEY,
                fitID INTEGER NOT NULL,
                linkType VARCHAR NOT NULL,
                strength INTEGER NOT NULL DEFAULT 0,
                mindlink BOOLEAN NOT NULL DEFAULT 0,
                active BOOLEAN NOT NULL DEFAULT 1,
                created DATETIME,
                modified DATETIME,
                FOREIGN KEY(fitID) REFERENCES fits(ID)
            );
        """)
        saveddata_engine.execute("CREATE INDEX ix_commandLinks_fitID ON commandLinks (fitID);")
