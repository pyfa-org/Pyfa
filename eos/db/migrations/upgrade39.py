"""
Migration 39

- Shield amplifier tiericide
- CCP getting rid of DB TDs due to exploits
"""

CONVERSIONS = {
    1798: (  # 'Basic' EM Shield Amplifier
        9562,  # Supplemental EM Ward Amplifier
    ),
    1804: (  # 'Basic' Explosive Shield Amplifier
        9574,  # Supplemental Explosive Deflection Amplifier
    ),
    1802: (  # 'Basic' Kinetic Shield Amplifier
        9570,  # Supplemental Kinetic Deflection Amplifier
    ),
    1800: (  # 'Basic' Thermal Shield Amplifier
        9566,  # Supplemental Thermal Dissipation Amplifier
    ),
    22933: (  # 'Investor' Tracking Disruptor I
        32416,  # Dark Blood Tracking Disruptor
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
