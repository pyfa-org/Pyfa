"""
Migration 22

- Adds the created and modified fields to most tables
"""
import sqlalchemy


def upgrade(saveddata_engine):

    # 1 = created only
    # 2 = created and modified
    tables = {
        "boosters": 2,
        "cargo": 2,
        "characters": 2,
        "crest": 1,
        "damagePatterns": 2,
        "drones": 2,
        "fighters": 2,
        "fits": 2,
        "projectedFits": 2,
        "commandFits": 2,
        "implants": 2,
        "implantSets": 2,
        "modules": 2,
        "overrides": 2,
        "characterSkills": 2,
        "targetResists": 2
    }

    for table in tables.keys():

        # midnight brain, there's probably a much more simple way to do this, but fuck it
        if tables[table] > 0:
            try:
                saveddata_engine.execute("SELECT created FROM {0} LIMIT 1;".format(table))
            except sqlalchemy.exc.DatabaseError:
                saveddata_engine.execute("ALTER TABLE {} ADD COLUMN created DATETIME;".format(table))

        if tables[table] > 1:
            try:
                saveddata_engine.execute("SELECT modified FROM {0} LIMIT 1;".format(table))
            except sqlalchemy.exc.DatabaseError:
                saveddata_engine.execute("ALTER TABLE {} ADD COLUMN modified DATETIME;".format(table))
