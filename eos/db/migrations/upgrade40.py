"""
Migration 40

Imports all item conversions since Migration 28 and runs them against module.baseItemID. This column seems to have been
forgotten about since it's been added.

"""
from .upgrade36 import CONVERSIONS as u36
from .upgrade37 import CONVERSIONS as u37
from .upgrade38 import CONVERSIONS as u38
from .upgrade39 import CONVERSIONS as u39

def upgrade(saveddata_engine):
    for conversions in [u36, u37, u38, u39]:
        for replacement_item, list in conversions.items():
            for retired_item in list:
                saveddata_engine.execute('UPDATE "modules" SET "baseItemID" = ? WHERE "baseItemID" = ?',
                               (replacement_item, retired_item))
