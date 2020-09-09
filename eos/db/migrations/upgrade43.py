"""
Migration 43

- Shield booster amplifier tiericide
"""

CONVERSIONS = {
    16533: (  # Stalwart Restrained Shield Boost Amplifier
        16531,  # 5a Prototype Shield Support I
    ),
    16535: (  # Copasetic Compact Shield Boost Amplifier
        16529,  # Ionic Field Accelerator I
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
