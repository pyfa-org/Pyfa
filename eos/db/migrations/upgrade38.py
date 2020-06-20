"""
Migration 38

- Armor hardener tiericide
"""

CONVERSIONS = {
    16357: (  # Experimental Enduring EM Armor Hardener I
        16353,  # Upgraded Armor EM Hardener I
    ),
    16365: (  # Experimental Enduring Explosive Armor Hardener I
        16361,  # Upgraded Armor Explosive Hardener I
    ),
    16373: (  # Experimental Enduring Kinetic Armor Hardener I
        16369,  # Upgraded Armor Kinetic Hardener I
    ),
    16381: (  # Experimental Enduring Thermal Armor Hardener I
        16377,  # Upgraded Armor Thermal Hardener I
    ),
    16359: (  # Prototype Compact EM Armor Hardener I
        16355,  # Limited Armor EM Hardener I
    ),
    16367: (  # Prototype Compact Explosive Armor Hardener I
        16363,  # Limited Armor Explosive Hardener I
    ),
    16375: (  # Prototype Compact Kinetic Armor Hardener I
        16371,  # Limited Armor Kinetic Hardener I
    ),
    16383: (  # Prototype Compact Thermal Armor Hardener I
        16379,  # Limited Armor Thermal Hardener I
    )
}


def upgrade(saveddata_engine):
    # Convert modules
    for replacement_item, list in CONVERSIONS.items():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
