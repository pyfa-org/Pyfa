"""
Migration 5

Simply deletes damage profiles with a blank name. See GH issue #256
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute('DELETE FROM damagePatterns WHERE name LIKE ?', ("",))
