"""
Migration 44

- Signal distortion amplifier tiericide
"""

CONVERSIONS = {
    25565: (  # Hypnos Compact Signal Distortion Amplifier I
        25571,  # Initiated Signal Distortion Amplifier I
        25569,  # Induced Signal Distortion Amplifier I
        25567,  # Compulsive Signal Distortion Amplifier I
    ),
}


def upgrade(saveddata_engine):
    # Convert modules
    for replacement_item, list in CONVERSIONS.items():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "modules" SET "baseItemID" = ? WHERE "baseItemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
