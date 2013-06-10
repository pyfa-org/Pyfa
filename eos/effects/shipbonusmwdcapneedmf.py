# Used by:
# Ship: Hyena
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Frigate").level
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "capacitorCapacityMultiplier", ship.getModifiedItemAttr("shipBonusMF") * level)
