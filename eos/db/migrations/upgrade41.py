"""
Migration 41

- Resistance plating tiericide
"""

CONVERSIONS = {
    16345: (  # Upgraded Layered Coating I
        16347,  # Limited Layered Plating I
        16349,  # 'Scarab' Layered Plating I
        16351,  # 'Grail' Layered Plating I
    ),
    16305: (  # Upgraded Multispectrum Coating I
        16307,  # Limited Adaptive Nano Plating I
        16309,  # 'Collateral' Adaptive Nano Plating I
        16311,  # 'Refuge' Adaptive Nano Plating I
    ),
    16329: (  # Upgraded EM Coating I
        16331,  # Limited EM Plating I
        16333,  # 'Contour' EM Plating I
        16335,  # 'Spiegel' EM Plating I
    ),
    16321: (  # Upgraded Explosive Coating I
        16323,  # Limited Explosive Plating I
        16325,  # Experimental Explosive Plating I
        16319,  # 'Aegis' Explosive Plating I
    ),
    16313: (  # Upgraded Kinetic Coating I
        16315,  # Limited Kinetic Plating I
        16317,  # Experimental Kinetic Plating I
        16327,  # 'Element' Kinetic Plating I
    ),
    16337: (  # Upgraded Thermal Coating I
        16339,  # Limited Thermal Plating I
        16341,  # Experimental Thermal Plating I
        16343,  # Prototype Thermal Plating I
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
