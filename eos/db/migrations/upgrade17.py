"""
Migration 17

- Moves all fleet boosters to the new schema
"""

from eos.db.sqlAlchemy import sqlAlchemy
from eos.db.saveddata.mapper import Fits


def upgrade(saveddata_engine):
    sql = """
          SELECT sm.memberID as boostedFit, s.leaderID AS squadBoost, w.leaderID AS wingBoost, g.leaderID AS gangBoost
          FROM squadmembers sm
          JOIN squads s ON s.ID = sm.squadID
          JOIN wings w on w.ID = s.wingID
          JOIN gangs g on g.ID = w.gangID
          """

    results = sqlAlchemy.saveddata_session.execute(sql)

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
                sqlAlchemy.saveddata_session.execute(Fits.commandFits_table.insert(),
                                          {"boosterID": value, "boostedID": boosted, "active": 1})
            except Exception:
                pass
        sqlAlchemy.saveddata_session.commit()
