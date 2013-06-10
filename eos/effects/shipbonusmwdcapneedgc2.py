# Used by:
# Ship: Deimos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                     "capacitorCapacityMultiplier", ship.getModifiedItemAttr("shipBonusGC2") * level)
