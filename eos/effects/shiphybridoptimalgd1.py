# Used by:
# Ship: Eris
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGD1") * level)
