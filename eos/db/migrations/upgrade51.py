"""
Migration 51

- Herald and Penitence were added to pyfa ahead of their release, under made-up type IDs. Move fits and
  everything else referencing those over to the type IDs CCP gave them.
"""

CONVERSIONS = {
    97793: (  # Herald
        1000000,  # Herald (pyfa preview)
    ),
    97904: (  # Penitence
        1000001,  # Penitence (pyfa preview)
    ),
}


def upgrade(saveddata_engine):
    for replacement_item, retired_items in CONVERSIONS.items():
        for retired_item in retired_items:
            saveddata_engine.execute('UPDATE "fits" SET "shipID" = ? WHERE "shipID" = ?',
                                     (replacement_item, retired_item))
