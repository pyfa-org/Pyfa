"""
Migration 19

- Deletes broken references to fits from the commandFits table (see GH issue #844)
"""


def upgrade(saveddata_engine):
    from eos.db import saveddata_session

    sql = """
        DELETE FROM commandFits
        WHERE boosterID NOT IN (select ID from fits)
        OR boostedID NOT IN (select ID from fits)
        """

    saveddata_session.execute(sql)
    saveddata_session.commit()
