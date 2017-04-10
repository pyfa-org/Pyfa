"""
Migration 9

Effectively drops UNIQUE constraint from boosters table. SQLite does not support
this, so we have to copy the table to the updated schema and then rename it
"""

tmpTable = """
CREATE TABLE boostersTemp (
    'ID' INTEGER NOT NULL,
    'itemID' INTEGER,
    'fitID' INTEGER NOT NULL,
    'active' BOOLEAN,
    PRIMARY KEY(ID),
    FOREIGN KEY('fitID') REFERENCES fits ('ID')
)
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute(tmpTable)
    saveddata_engine.execute(
            "INSERT INTO boostersTemp (ID, itemID, fitID, active) SELECT ID, itemID, fitID, active FROM boosters")
    saveddata_engine.execute("DROP TABLE boosters")
    saveddata_engine.execute("ALTER TABLE boostersTemp RENAME TO boosters")
