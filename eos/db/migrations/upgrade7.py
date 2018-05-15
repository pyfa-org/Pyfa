"""
Migration 7

- Converts Scorpion Ishukone Watch to Scorpion

    Mosaic introduced proper skinning system, and Ishukone Scorp
    was the only ship which was presented as stand-alone ship in
    Pyfa.
"""

CONVERSIONS = {
    640: (  # Scorpion
        4005,  # Scorpion Ishukone Watch
    )
}


def upgrade(saveddata_engine):
    # Convert ships
    for replacement_item, list in CONVERSIONS.items():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "fits" SET "shipID" = ? WHERE "shipID" = ?',
                                     (replacement_item, retired_item))
