"""
Migration 4

- Converts modules based on Proteus Module Tiericide
    Some modules have been unpublished (and unpublished module attributes are removed
    from database), which causes pyfa to crash. We therefore replace these
    modules with their new replacements

    Based on http://community.eveonline.com/news/patch-notes/patch-notes-for-proteus/
    and output of itemDiff.py
"""

CONVERSIONS = {
    506  : (  # 'Basic' Capacitor Power Relay
        8205,  # Alpha Reactor Control: Capacitor Power Relay
        8209,  # Marked Generator Refitting: Capacitor Power Relay
        8203,  # Partial Power Plant Manager: Capacity Power Relay
        8207,  # Type-E Power Core Modification: Capacitor Power Relay
    ),
    8177 : (  # Mark I Compact Capacitor Power Relay
        8173,  # Beta Reactor Control: Capacitor Power Relay I
    ),
    8175 : (  # Type-D Restrained Capacitor Power Relay
        8171,  # Local Power Plant Manager: Capacity Power Relay I
    ),

    421  : (  # 'Basic' Capacitor Recharger
        4425,  # AGM Capacitor Charge Array,
        4421,  # F-a10 Buffer Capacitor Regenerator
        4423,  # Industrial Capacitor Recharger
        4427,  # Secondary Parallel Link-Capacitor
    ),
    4435 : (  # Eutectic Compact Cap Recharger
        4433,  # Barton Reactor Capacitor Recharger I
        4431,  # F-b10 Nominal Capacitor Regenerator
        4437,  # Fixed Parallel Link-Capacitor I
    ),

    1315 : (  # 'Basic' Expanded Cargohold
        5483,  # Alpha Hull Mod Expanded Cargo
        5479,  # Marked Modified SS Expanded Cargo
        5481,  # Partial Hull Conversion Expanded Cargo
        5485,  # Type-E Altered SS Expanded Cargo
    ),
    5493 : (  # Type-D Restrained Expanded Cargo
        5491,  # Beta Hull Mod Expanded Cargo
        5489,  # Local Hull Conversion Expanded Cargo I
        5487,  # Mark I Modified SS Expanded Cargo
    ),

    1401 : (  # 'Basic' Inertial Stabilizers
        5523,  # Alpha Hull Mod Inertial Stabilizers
        5521,  # Partial Hull Conversion Inertial Stabilizers
        5525,  # Type-E Altered SS Inertial Stabilizers
    ),
    5533 : (  # Type-D Restrained Inertial Stabilizers
        5531,  # Beta Hull Mod Inertial Stabilizers
        5529,  # Local Hull Conversion Inertial Stabilizers I
        5527,  # Mark I Modified SS Inertial Stabilizers
        5519,  # Marked Modified SS Inertial Stabilizers
    ),

    5239 : (  # EP-S Gaussian Scoped Mining Laser
        5241,  # Dual Diode Mining Laser I
    ),
    5233 : (  # Single Diode Basic Mining Laser
        5231,  # EP-R Argon Ion Basic Excavation Pulse
        5237,  # Rubin Basic Particle Bore Stream
        5235,  # Xenon Basic Drilling Beam
    ),
    5245 : (  # Particle Bore Compact Mining Laser
        5243,  # XeCl Drilling Beam I
    ),

    22619: (  # Frigoris Restrained Ice Harvester Upgrade
        22617,  # Crisium Ice Harvester Upgrade
    ),
    22611: (  # Elara Restrained Mining Laser Upgrade
        22609,  # Erin Mining Laser Upgrade
    ),

    1242 : (  # 'Basic' Nanofiber Internal Structure
        5591,  # Alpha Hull Mod Nanofiber Structure
        5595,  # Marked Modified SS Nanofiber Structure
        5559,  # Partial Hull Conversion Nanofiber Structure
        5593,  # Type-E Altered SS Nanofiber Structure
    ),
    5599 : (  # Type-D Restrained Nanofiber Structure
        5597,  # Beta Hull Mod Nanofiber Structure
        5561,  # Local Hull Conversion Nanofiber Structure I
        5601,  # Mark I Modified SS Nanofiber Structure
    ),

    1192 : (  # 'Basic' Overdrive Injector System
        5613,  # Alpha Hull Mod Overdrive Injector
        5617,  # Marked Modified SS Overdrive Injector
        5611,  # Partial Hull Conversion Overdrive Injector
        5615,  # Type-E Altered SS Overdrive Injector
    ),
    5631 : (  # Type-D Restrained Overdrive Injector
        5629,  # Beta Hull Mod Overdrive Injector
        5627,  # Local Hull Conversion Overdrive Injector I
        5633,  # Mark I Modified SS Overdrive Injector
    ),

    1537 : (  # 'Basic' Power Diagnostic System
        8213,  # Alpha Reactor Control: Diagnostic System
        8217,  # Marked Generator Refitting: Diagnostic System
        8211,  # Partial Power Plant Manager: Diagnostic System
        8215,  # Type-E Power Core Modification: Diagnostic System
        8255,  # Type-E Power Core Modification: Reaction Control
    ),
    8225 : (  # Mark I Compact Power Diagnostic System
        8221,  # Beta Reactor Control: Diagnostic System I
        8219,  # Local Power Plant Manager: Diagnostic System I
        8223,  # Type-D Power Core Modification: Diagnostic System
    ),

    1240 : (  # 'Basic' Reinforced Bulkheads
        5677,  # Alpha Hull Mod Reinforced Bulkheads
        5681,  # Marked Modified SS Reinforced Bulkheads
        5675,  # Partial Hull Conversion Reinforced Bulkheads
        5679,  # Type-E Altered SS Reinforced Bulkheads
    ),
    5649 : (  # Mark I Compact Reinforced Bulkheads
        5645,  # Beta Hull Mod Reinforced Bulkheads
    ),
    5647 : (  # Type-D Restrained Reinforced Bulkheads
        5643,  # Local Hull Conversion Reinforced Bulkheads I
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
