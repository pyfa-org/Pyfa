"""
Migration 50

- Add vaults table and vaultID to fits. All existing fits are assigned to the Default vault.
"""

import sqlalchemy


def upgrade(saveddata_engine):
    # Create vaults table
    try:
        saveddata_engine.execute("SELECT ID FROM vaults LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("""
            CREATE TABLE vaults (
                "ID" INTEGER NOT NULL PRIMARY KEY,
                name VARCHAR NOT NULL,
                "sortOrder" INTEGER NOT NULL DEFAULT 0
            )
        """)
        saveddata_engine.execute("INSERT INTO vaults (name, \"sortOrder\") VALUES ('Default', 0)")

    # Add vaultID column to fits
    try:
        saveddata_engine.execute("SELECT vaultID FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN vaultID INTEGER REFERENCES vaults(ID)")

    # Assign every existing fit to the default vault so no data is lost
    saveddata_engine.execute(
        "UPDATE fits SET vaultID = (SELECT ID FROM vaults LIMIT 1) WHERE vaultID IS NULL"
    )
