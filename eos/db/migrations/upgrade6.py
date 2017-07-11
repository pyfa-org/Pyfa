"""
Migration 6

Overwrites damage profile 0 to reset bad uniform values (bad values set with bug)
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute('DELETE FROM damagePatterns WHERE name LIKE ? OR ID LIKE ?', ("Uniform", "1"))
    saveddata_engine.execute('INSERT INTO damagePatterns (ID, name, emAmount, thermalAmount, kineticAmount, explosiveAmount, ownerID) VALUES (?, ?, ?, ?, ?, ?, ?)',
                             (1, "Uniform", 25, 25, 25, 25, None))
