"""
Migration 42

- Resistance membrane tiericide
"""

CONVERSIONS = {
    16391: (  # Compact Multispectrum Energized Membrane
        16389,  # Experimental Energized Adaptive Nano Membrane I
        16387,  # Limited Energized Adaptive Nano Membrane I
        16385,  # Upgraded Energized Adaptive Nano Membrane I
    ),
    16423: (  # Compact Layered Energized Membrane
        16421,  # Experimental Energized Armor Layering Membrane I
        16419,  # Limited Energized Armor Layering Membrane I
        16417,  # Upgraded Energized Armor Layering Membrane I
    ),
    16415: (  # Compact EM Energized Membrane
        16413,  # Experimental Energized EM Membrane I
        16411,  # Limited Energized EM Membrane I
        16409,  # Upgraded Energized EM Membrane I
    ),
    16407: (  # Compact Explosive Energized Membrane
        16405,  # Experimental Energized Explosive Membrane I
        16403,  # Limited Energized Explosive Membrane I
        16401,  # Upgraded Energized Explosive Membrane I
    ),
    16399: (  # Compact Kinetic Energized Membrane
        16397,  # Experimental Energized Kinetic Membrane I
        16395,  # Limited Energized Kinetic Membrane I
        16393,  # Upgraded Energized Kinetic Membrane I
    ),
    16431: (  # Compact Thermal Energized Membrane
        16429,  # Experimental Energized Thermal Membrane I
        16427,  # Limited Energized Thermal Membrane I
        16425,  # Upgraded Energized Thermal Membrane I
    )
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
