"""
Migration 37

- Capacitor Booster tiericide
"""

CONVERSIONS = {
    4959: (  # 'Seed' Micro Capacitor Booster I
        4957,  # Micro Brief Capacitor Overcharge I
        4961,  # Micro Tapered Capacitor Infusion I
        4955,  # Micro F-RX Prototype Capacitor Boost
        3556,  # Micro Capacitor Booster I
        3558,  # Micro Capacitor Booster II
        15774,  # Ammatar Navy Micro Capacitor Booster
        14180,  # Dark Blood Micro Capacitor Booster
        14182,  # True Sansha Micro Capacitor Booster
        15782,  # Imperial Navy Micro Capacitor Booster
    ),
    5011: (  # Small F-RX Compact Capacitor Booster
        5009,  # Small Brief Capacitor Overcharge I
        5013,  # Small Tapered Capacitor Infusion I
        5007,  # Small F-RX Prototype Capacitor Boost
    ),
    4833: (  # Medium F-RX Compact Capacitor Booster
        4831,  # Medium Brief Capacitor Overcharge I
        4835,  # Medium Tapered Capacitor Infusion I
        4829,  # Medium F-RX Prototype Capacitor Boost
    ),
    5051: (  # Heavy F-RX Compact Capacitor Booster
        5049,  # Heavy Brief Capacitor Overcharge I
        5053,  # Heavy Tapered Capacitor Infusion I
        5047,  # Heavy F-RX Prototype Capacitor Boost
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
