"""
Migration 36

- Shield Booster, Armor Repairer and Capacitor Transfer tiericide
"""

CONVERSIONS = {
    6441: (  # Small Clarity Ward Enduring Shield Booster
        6443,  # Small Converse Deflection Catalyzer
    ),
    6437: (  # Small C5-L Compact Shield Booster
        6439,  # Small Neutron Saturation Injector I
    ),
    10868: (  # Medium Clarity Ward Enduring Shield Booster
        10870,  # Medium Converse Deflection Catalyzer
    ),
    10872: (  # Medium C5-L Compact Shield Booster
        10866,  # Medium Neutron Saturation Injector I
    ),
    10876: (  # Large Clarity Ward Enduring Shield Booster
        10878,  # Large Converse Deflection Catalyzer
    ),
    10880: (  # Large C5-L Compact Shield Booster
        10874,  # Large Neutron Saturation Injector I
    ),
    10884: (  # X-Large Clarity Ward Enduring Shield Booster
        10886,  # X-Large Converse Deflection Catalyzer
    ),
    10888: (  # X-Large C5-L Compact Shield Booster
        10882,  # X-Large Neutron Saturation Injector I
    ),
    4533: (  # Small ACM Compact Armor Repairer
        4531,  # Small Inefficient Armor Repair Unit
    ),
    4529: (  # Small I-a Enduring Armor Repairer
        4535,  # Small Automated Carapace Restoration
    ),
    4573: (  # Medium ACM Compact Armor Repairer
        4571,  # Medium Inefficient Armor Repair Unit
    ),
    4569: (  # Medium I-a Enduring Armor Repairer
        4575,  # Medium Automated Carapace Restoration
    ),
    22889: (  # 'Meditation' Medium Armor Repairer I
        4579,  # Medium Nano Armor Repair Unit I
    ),
    4613: (  # Large ACM Compact Armor Repairer
        4611,  # Large Inefficient Armor Repair Unit
    ),
    4609: (  # Large I-a Enduring Armor Repairer
        4615,  # Large Automated Carapace Restoration
    ),
    22891: (  # 'Protest' Large Armor Repairer I
        4621,  # Large 'Reprieve' Vestment Reconstructer I
    ),
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
