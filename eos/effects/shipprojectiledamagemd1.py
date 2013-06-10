# Used by:
# Variations of ship: Thrasher (3 of 3)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMD1") * level)
