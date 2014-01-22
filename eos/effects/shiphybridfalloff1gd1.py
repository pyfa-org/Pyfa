# Used by:
# Ships named like: Catalyst (6 of 6)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGD1") * level)
