"""
Migration 26

- Deletes invalid command fit relationships caused by a bug (see #1244)
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute("DELETE FROM commandFits WHERE boosterID NOT IN (SELECT ID FROM fits) OR boostedID NOT IN (SELECT ID FROM fits)")
