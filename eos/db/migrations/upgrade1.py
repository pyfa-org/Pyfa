"""
Migration 1

- Alters fits table to introduce target resist attribute
- Converts modules based on Oceanus Module Tiericide
    Some modules have been deleted, which causes pyfa to crash when fits are
    loaded as they no longer exist in the database. We therefore replace these
    modules with their new replacements

    Based on http://community.eveonline.com/news/patch-notes/patch-notes-for-oceanus/
    and output of itemDiff.py
"""

import sqlalchemy

CONVERSIONS = {
    6135 : [  # Scoped Cargo Scanner
        6133,  # Interior Type-E Cargo Identifier
    ],
    6527 : [  # Compact Ship Scanner
        6525,  # Ta3 Perfunctory Vessel Probe
        6529,  # Speculative Ship Identifier I
        6531,  # Practical Type-E Ship Probe
    ],
    6569 : [  # Scoped Survey Scanner
        6567,  # ML-3 Amphilotite Mining Probe
        6571,  # Rock-Scanning Sensor Array I
        6573,  # 'Dactyl' Type-E Asteroid Analyzer
    ],
    509  : [  # 'Basic' Capacitor Flux Coil
        8163,  # Partial Power Plant Manager: Capacitor Flux
        8165,  # Alpha Reactor Control: Capacitor Flux
        8167,  # Type-E Power Core Modification: Capacitor Flux
        8169,  # Marked Generator Refitting: Capacitor Flux
    ],
    8135 : [  # Restrained Capacitor Flux Coil
        8131,  # Local Power Plant Manager: Capacitor Flux I
    ],
    8133 : [  # Compact Capacitor Flux Coil
        8137,  # Mark I Generator Refitting: Capacitor Flux
    ],
    3469 : [  # Basic Co-Processor
        8744,  # Nanoelectrical Co-Processor
        8743,  # Nanomechanical CPU Enhancer
        8746,  # Quantum Co-Processor
        8745,  # Photonic CPU Enhancer
        15425,  # Naiyon's Modified Co-Processor (never existed but convert
        # anyway as some fits may include it)
    ],
    8748 : [  # Upgraded Co-Processor
        8747,  # Nanomechanical CPU Enhancer I
        8750,  # Quantum Co-Processor I
        8749,  # Photonic CPU Enhancer I
    ],
    1351 : [  # Basic Reactor Control Unit
        8251,  # Partial Power Plant Manager: Reaction Control
        8253,  # Alpha Reactor Control: Reaction Control
        8257,  # Marked Generator Refitting: Reaction Control
    ],
    8263 : [  # Compact Reactor Control Unit
        8259,  # Local Power Plant Manager: Reaction Control I
        8265,  # Mark I Generator Refitting: Reaction Control
        8261,  # Beta Reactor Control: Reaction Control I
    ],
    16537: [  # Compact Micro Auxiliary Power Core
        16539,  # Micro B88 Core Augmentation
        16541,  # Micro K-Exhaust Core Augmentation
    ],
    31936: [  # Navy Micro Auxiliary Power Core
        16543,  # Micro 'Vigor' Core Augmentation
    ],
    8089 : [  # Compact Light Missile Launcher
        8093,  # Prototype 'Arbalest' Light Missile Launcher
    ],
    8091 : [  # Ample Light Missile Launcher
        7993,  # Experimental TE-2100 Light Missile Launcher
    ],
    # Surface Cargo Scanner I was removed from game, however no mention of
    # replacement module in patch notes. Morphing it to meta 0 module to be safe
    442  : [  # Cargo Scanner I
        6129,  # Surface Cargo Scanner I
    ]
}


def upgrade(saveddata_engine):
    # Update fits schema to include target resists attribute
    try:
        saveddata_engine.execute("SELECT targetResistsID FROM fits LIMIT 1")
    except sqlalchemy.exc.DatabaseError:
        saveddata_engine.execute("ALTER TABLE fits ADD COLUMN targetResistsID INTEGER;")

    # Convert modules
    for replacement_item, list in CONVERSIONS.items():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
