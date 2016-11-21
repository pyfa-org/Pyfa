"""
Migration 17

- Moves all fleet boosters to the new schema
"""

import sqlalchemy

def upgrade(saveddata_engine):

    sql = """
          SELECT sm.memberID as boostedFit, s.leaderID AS squadBoost, w.leaderID AS wingBoost, g.leaderID AS gangBoost
          FROM squadmembers sm
          JOIN squads s ON s.ID = sm.squadID
          JOIN wings w on w.ID = s.wingID
          JOIN gangs g on g.ID = w.gangID
          """
    with saveddata_engine.connect() as connection:
        results = saveddata_engine.execute(sql)


        for row in results:
            boosted = row["boostedFit"]
            types = ("squad", "wing", "gang")
            for x in types:
                value = row["{}Boost".format(x)]
                if value is None:
                    continue
                try:
                        connection.execute('INSERT INTO commandFits ("boosterID", "boostedID", "active") VALUES (?, ?, 1)', (value, boosted))
                except Exception, e:
                    continue
