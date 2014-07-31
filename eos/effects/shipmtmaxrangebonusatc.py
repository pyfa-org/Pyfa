# Used by:
# Ship: Mimir
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusATC2"))
