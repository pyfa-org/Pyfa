"""
Migration 27

- Resets all alpha clones to 1 (CCP consolidated all alpha's into one skillset)
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute("UPDATE characters SET alphaCloneID = 1 WHERE alphaCloneID IS NOT NULL")
