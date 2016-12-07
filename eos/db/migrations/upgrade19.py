"""
Migration 19

- Deletes broken references to fits from the commandFits table (see GH issue #844)
"""


def upgrade(saveddata_engine):
    from eos.db.sqlAlchemy import sqlAlchemy

    sql = """
          DELETE FROM commandFits
          WHERE boosterID NOT IN (select ID from fits)
          OR boostedID NOT IN (select ID from fits)
          """

    sqlAlchemy.saveddata_session.execute(sql)
    sqlAlchemy.saveddata_session.commit()
