"""
Migration 36

- Capacitor Transfer Tiericide
"""

CONVERSIONS = {
    5093: (  # Small Radiative Scoped Remote Capacitor Transmitter
        5087,  # Small Partial E95a Remote Capacitor Transmitter
    ),
    5091: (  # Small Inductive Compact Remote Capacitor Transmitter
        5089,  # Small Murky Remote Capacitor Transmitter
    ),
    16489: (  # Medium Radiative Scoped Remote Capacitor Transmitter
        16493,  # Medium Partial E95b Remote Capacitor Transmitter
    ),
    16495: (  # Medium Inductive Compact Remote Capacitor Transmitter
        16491,  # Medium Murky Remote Capacitor Transmitter
    ),
    16481: (  # Large Radiative Scoped Remote Capacitor Transmitter
        16485,  # Large Partial E95c Remote Capacitor Transmitter
    ),
    16487: (  # Large Inductive Compact Remote Capacitor Transmitter
        16483,  # Large Murky Remote Capacitor Transmitter
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
