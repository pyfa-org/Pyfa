"""
Migration 11

- Converts modules based on December Release 2015 Tiericide
    Some modules have been unpublished (and unpublished module attributes are removed
    from database), which causes pyfa to crash. We therefore replace these
    modules with their new replacements
"""

CONVERSIONS = {
    16467: (  # Medium Gremlin Compact Energy Neutralizer
        16471,  # Medium Unstable Power Fluctuator I
    ),
    22947: (  # 'Beatnik' Small Remote Armor Repairer
        23414,  # 'Brotherhood' Small Remote Armor Repairer
    ),
    8295 : (  # Type-D Restrained Shield Flux Coil
        8293,  # Beta Reactor Control: Shield Flux I
    ),
    16499: (  # Heavy Knave Scoped Energy Nosferatu
        16501,  # E500 Prototype Energy Vampire
    ),
    16477: (  # Heavy Infectious Scoped Energy Neutralizer
        16473,  # Heavy Rudimentary Energy Destabilizer I
    ),
    16475: (  # Heavy Gremlin Compact Energy Neutralizer
        16479,  # Heavy Unstable Power Fluctuator I
    ),
    16447: (  # Medium Solace Scoped Remote Armor Repairer
        16445,  # Medium 'Arup' Remote Armor Repairer
    ),
    508  : (  # 'Basic' Shield Flux Coil
        8325,  # Alpha Reactor Shield Flux
        8329,  # Marked Generator Refitting: Shield Flux
        8323,  # Partial Power Plant Manager: Shield Flux
        8327,  # Type-E Power Core Modification: Shield Flux
    ),
    1419 : (  # 'Basic' Shield Power Relay
        8341,  # Alpha Reactor Shield Power Relay
        8345,  # Marked Generator Refitting: Shield Power Relay
        8339,  # Partial Power Plant Manager: Shield Power Relay
        8343,  # Type-E Power Core Modification: Shield Power Relay
    ),
    16439: (  # Small Solace Scoped Remote Armor Repairer
        16437,  # Small 'Arup' Remote Armor Repairer
    ),
    16505: (  # Medium Ghoul Compact Energy Nosferatu
        16511,  # Medium Diminishing Power System Drain I
    ),
    8297 : (  # Mark I Compact Shield Flux Coil
        8291,  # Local Power Plant Manager: Reaction Shield Flux I
    ),
    16455: (  # Large Solace Scoped Remote Armor Repairer
        16453,  # Large 'Arup' Remote Armor Repairer
    ),
    6485 : (  # M51 Benefactor Compact Shield Recharger
        6491,  # Passive Barrier Compensator I
        6489,  # 'Benefactor' Ward Reconstructor
        6487,  # Supplemental Screen Generator I
    ),
    5137 : (  # Small Knave Scoped Energy Nosferatu
        5135,  # E5 Prototype Energy Vampire
    ),
    8579 : (  # Medium Murky Compact Remote Shield Booster
        8581,  # Medium 'Atonement' Remote Shield Booster
    ),
    8531 : (  # Small Murky Compact Remote Shield Booster
        8533,  # Small 'Atonement' Remote Shield Booster
    ),
    16497: (  # Heavy Ghoul Compact Energy Nosferatu
        16503,  # Heavy Diminishing Power System Drain I
    ),
    4477 : (  # Small Gremlin Compact Energy Neutralizer
        4475,  # Small Unstable Power Fluctuator I
    ),
    8337 : (  # Mark I Compact Shield Power Relay
        8331,  # Local Power Plant Manager: Reaction Shield Power Relay I
    ),
    23416: (  # 'Peace' Large Remote Armor Repairer
        22951,  # 'Pacifier' Large Remote Armor Repairer
    ),
    5141 : (  # Small Ghoul Compact Energy Nosferatu
        5139,  # Small Diminishing Power System Drain I
    ),
    4471 : (  # Small Infectious Scoped Energy Neutralizer
        4473,  # Small Rudimentary Energy Destabilizer I
    ),
    16469: (  # Medium Infectious Scoped Energy Neutralizer
        16465,  # Medium Rudimentary Energy Destabilizer I
    ),
    8335 : (  # Type-D Restrained Shield Power Relay
        8333,  # Beta Reactor Control: Shield Power Relay I
    ),
    405  : (  # 'Micro' Remote Shield Booster
        8631,  # Micro Asymmetric Remote Shield Booster
        8627,  # Micro Murky Remote Shield Booster
        8629,  # Micro 'Atonement' Remote Shield Booster
        8633,  # Micro S95a Remote Shield Booster
    ),
    8635 : (  # Large Murky Compact Remote Shield Booster
        8637,  # Large 'Atonement' Remote Shield Booster
    ),
    16507: (  # Medium Knave Scoped Energy Nosferatu
        16509,  # E50 Prototype Energy Vampire
    ),
}


def upgrade(saveddata_engine):
    # Convert modules
    for replacement_item, list in CONVERSIONS.iteritems():
        for retired_item in list:
            saveddata_engine.execute('UPDATE "modules" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
            saveddata_engine.execute('UPDATE "cargo" SET "itemID" = ? WHERE "itemID" = ?',
                                     (replacement_item, retired_item))
