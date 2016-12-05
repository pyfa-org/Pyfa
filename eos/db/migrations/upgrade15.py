"""
Migration 15

- Delete projected modules on citadels
"""


def upgrade(saveddata_engine):
    sql = """
    DELETE FROM modules WHERE ID IN
    (
        SELECT m.ID FROM modules AS m
        JOIN fits AS f ON m.fitID = f.ID
        WHERE f.shipID IN ("35832", "35833", "35834", "40340")
        AND m.projected = 1
    )
    """

    saveddata_engine.execute(sql)
