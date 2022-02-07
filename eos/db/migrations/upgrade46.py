"""
Migration 46

- Mining crystal changes
"""

CONVERSIONS = {
    60276: (  # Simple Asteroid Mining Crystal Type A I
        18066,  # Veldspar Mining Crystal I
        18062,  # Scordite Mining Crystal I
        18060,  # Pyroxeres Mining Crystal I
        18058,  # Plagioclase Mining Crystal I
    ),
    60281: (  # Simple Asteroid Mining Crystal Type A II
        18618,  # Veldspar Mining Crystal II
        18616,  # Scordite Mining Crystal II
        18614,  # Pyroxeres Mining Crystal II
        18612,  # Plagioclase Mining Crystal II
    ),
    60285: (  # Coherent Asteroid Mining Crystal Type A I
        18056,  # Omber Mining Crystal I
        18052,  # Kernite Mining Crystal I
        18050,  # Jaspet Mining Crystal I
        18048,  # Hemorphite Mining Crystal I
        18046,  # Hedbergite Mining Crystal I
    ),
    60288: (  # Coherent Asteroid Mining Crystal Type A II
        18610,  # Omber Mining Crystal II
        18604,  # Jaspet Mining Crystal II
        18606,  # Kernite Mining Crystal II
        18600,  # Hedbergite Mining Crystal II
        18602,  # Hemorphite Mining Crystal II
    ),
    60291: (  # Variegated Asteroid Mining Crystal Type A I
        18044,  # Gneiss Mining Crystal I
        18042,  # Dark Ochre Mining Crystal I
        18040,  # Crokite Mining Crystal I
    ),
    60294: (  # Variegated Asteroid Mining Crystal Type A II
        18598,  # Gneiss Mining Crystal II
        18596,  # Dark Ochre Mining Crystal II
        18594,  # Crokite Mining Crystal II
    ),
    60297: (  # Complex Asteroid Mining Crystal Type A I
        18038,  # Bistot Mining Crystal I
        18036,  # Arkonor Mining Crystal I
        18064,  # Spodumain Mining Crystal I
    ),
    60300: (  # Complex Asteroid Mining Crystal Type A II
        18592,  # Bistot Mining Crystal II
        18590,  # Arkonor Mining Crystal II
        18624,  # Spodumain Mining Crystal II
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
            saveddata_engine.execute('UPDATE "modules" SET "chargeID" = ? WHERE "chargeID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
