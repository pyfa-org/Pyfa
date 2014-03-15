# Used by:
# Ships named like: Thrasher (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))
