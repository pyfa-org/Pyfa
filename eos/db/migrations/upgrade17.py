"""
Migration 17

- Moves all fleet boosters to the new schema
"""


def upgrade(saveddata_engine):
    from eos.db import saveddata_session
    from eos.db.saveddata.fit import commandFits_table

    sql = """
          SELECT sm.memberID as boostedFit, s.leaderID AS squadBoost, w.leaderID AS wingBoost, g.leaderID AS gangBoost
          FROM squadmembers sm
          JOIN squads s ON s.ID = sm.squadID
          JOIN wings w on w.ID = s.wingID
          JOIN gangs g on g.ID = w.gangID
          """
    try:
        results = saveddata_session.execute(sql)

        inserts = []

        for row in results:
            boosted = row["boostedFit"]
            types = ("squad", "wing", "gang")
            for x in types:
                value = row["{}Boost".format(x)]
                if value is None:
                    continue

                inserts.append({"boosterID": value, "boostedID": boosted, "active": 1})
                try:
                    saveddata_session.execute(commandFits_table.insert(),
                                              {"boosterID": value, "boostedID": boosted, "active": 1})
                except Exception:
                    pass
        saveddata_session.commit()
    except:
        # Shouldn't fail unless you have updated database without the old fleet schema and manually modify the database version
        # If it does, simply fail. Fleet data migration isn't critically important here
        pass
