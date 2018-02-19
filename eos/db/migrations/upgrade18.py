"""
Migration 8

- Converts modules from old Warfare Links to Command Modules
"""

CONVERSIONS = {
    42526: (  # Armor Command Burst I
        20069,  # Armored Warfare Link - Damage Control I
        20409,  # Armored Warfare Link - Passive Defense I
        22227,  # Armored Warfare Link - Rapid Repair I
    ),
    43552: (  # Armor Command Burst II
        4264,  # Armored Warfare Link - Damage Control II
        4266,  # Armored Warfare Link - Passive Defense II
        4266,  # Armored Warfare Link - Rapid Repair II
    ),
    42527: (  # Information Command Burst I
        11052,  # Information Warfare Link - Sensor Integrity I
        20405,  # Information Warfare Link - Recon Operation I
        20406,  # Information Warfare Link - Electronic Superiority I
    ),
    43554: (  # Information Command Burst II
        4268,  # Information Warfare Link - Electronic Superiority II
        4270,  # Information Warfare Link - Recon Operation II
        4272,  # Information Warfare Link - Sensor Integrity II
    ),
    42529: (  # Shield Command Burst I
        20124,  # Siege Warfare Link - Active Shielding I
        20514,  # Siege Warfare Link - Shield Harmonizing I
        22228,  # Siege Warfare Link - Shield Efficiency I
    ),
    43555: (  # Shield Command Burst II
        4280,  # Siege Warfare Link - Active Shielding II
        4282,  # Siege Warfare Link - Shield Efficiency II
        4284  # Siege Warfare Link - Shield Harmonizing II
    ),
    42530: (  # Skirmish Command Burst I
        11017,  # Skirmish Warfare Link - Interdiction Maneuvers I
        20070,  # Skirmish Warfare Link - Evasive Maneuvers I
        20408,  # Skirmish Warfare Link - Rapid Deployment I
    ),
    43556: (  # Skirmish Command Burst II
        4286,  # Skirmish Warfare Link - Evasive Maneuvers II
        4288,  # Skirmish Warfare Link - Interdiction Maneuvers II
        4290  # Skirmish Warfare Link - Rapid Deployment II
    ),
    42528: (  # Mining Foreman Burst I
        22553,  # Mining Foreman Link - Harvester Capacitor Efficiency I
        22555,  # Mining Foreman Link - Mining Laser Field Enhancement I
        22557,  # Mining Foreman Link - Laser Optimization I
    ),
    43551: (  # Mining Foreman Burst II
        4274,  # Mining Foreman Link - Harvester Capacitor Efficiency II
        4276,  # Mining Foreman Link - Laser Optimization II
        4278  # Mining Foreman Link - Mining Laser Field Enhancement II
    ),
}


def upgrade(saveddata_engine):
    # Convert modules
    for replacement_item, list in CONVERSIONS.items():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
