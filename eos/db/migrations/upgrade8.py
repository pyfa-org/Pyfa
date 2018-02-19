"""
Migration 8

- Converts modules based on Carnyx Module Tiericide
    Some modules have been unpublished (and unpublished module attributes are removed
    from database), which causes pyfa to crash. We therefore replace these
    modules with their new replacements
"""

CONVERSIONS = {
    8529 : (  # Large F-S9 Regolith Compact Shield Extender
        8409,  # Large Subordinate Screen Stabilizer I
    ),
    8419 : (  # Large Azeotropic Restrained Shield Extender
        8489,  # Large Supplemental Barrier Emitter I
    ),
    8517 : (  # Medium F-S9 Regolith Compact Shield Extender
        8397,  # Medium Subordinate Screen Stabilizer I
    ),
    8433 : (  # Medium Azeotropic Restrained Shield Extender
        8477,  # Medium Supplemental Barrier Emitter I
    ),
    20627: (  # Small 'Trapper' Shield Extender
        8437,  # Micro Azeotropic Ward Salubrity I
        8505,  # Micro F-S9 Regolith Shield Induction
        3849,  # Micro Shield Extender I
        3851,  # Micro Shield Extender II
        8387,  # Micro Subordinate Screen Stabilizer I
        8465,  # Micro Supplemental Barrier Emitter I
    ),
    8521 : (  # Small F-S9 Regolith Compact Shield Extender
        8401,  # Small Subordinate Screen Stabilizer I
    ),
    8427 : (  # Small Azeotropic Restrained Shield Extender
        8481,  # Small Supplemental Barrier Emitter I
    ),
    11343: (  # 100mm Crystalline Carbonide Restrained Plates
        11345,  # 100mm Reinforced Nanofiber Plates I
    ),
    11341: (  # 100mm Rolled Tungsten Compact Plates
        11339,  # 100mm Reinforced Titanium Plates I
    ),
    11327: (  # 1600mm Crystalline Carbonide Restrained Plates
        11329,  # 1600mm Reinforced Nanofiber Plates I
    ),
    11325: (  # 1600mm Rolled Tungsten Compact Plates
        11323,  # 1600mm Reinforced Titanium Plates I
    ),
    11351: (  # 200mm Crystalline Carbonide Restrained Plates
        11353,  # 200mm Reinforced Nanofiber Plates I
    ),
    11349: (  # 200mm Rolled Tungsten Compact Plates
        11347,  # 200mm Reinforced Titanium Plates I
    ),
    11311: (  # 400mm Crystalline Carbonide Restrained Plates
        11313,  # 400mm Reinforced Nanofiber Plates I
    ),
    11309: (  # 400mm Rolled Tungsten Compact Plates
        11307,  # 400mm Reinforced Titanium Plates I
    ),
    23791: (  # 'Citadella' 100mm Steel Plates
        11335,  # 50mm Reinforced Crystalline Carbonide Plates I
        11337,  # 50mm Reinforced Nanofiber Plates I
        11333,  # 50mm Reinforced Rolled Tungsten Plates I
        11291,  # 50mm Reinforced Steel Plates I
        20343,  # 50mm Reinforced Steel Plates II
        11331,  # 50mm Reinforced Titanium Plates I
    ),
    11319: (  # 800mm Crystalline Carbonide Restrained Plates
        11321,  # 800mm Reinforced Nanofiber Plates I
    ),
    11317: (  # 800mm Rolled Tungsten Compact Plates
        11315,  # 800mm Reinforced Titanium Plates I
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
